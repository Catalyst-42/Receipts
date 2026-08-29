from typing import Any

from fastapi import HTTPException, status
from fastapi.responses import StreamingResponse
from httpx import AsyncClient, ConnectError, TimeoutException
from pydantic import UUID7
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.core.transactional import transactional
from src.crpt.dao import CrptDao
from src.crpt.schemes import Crpt, CrptList
from src.receipts.schemes import FiscalFields
from src.core.schemes import Count


class CrptService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.crpt_dao = CrptDao(db)

    async def get_all(self) -> CrptList:
        result = await self.crpt_dao.get_all()
        return CrptList(items=[Crpt.model_validate(item) for item in result])

    async def get_by_id(self, crpt_id: UUID7) -> Crpt:
        result = await self.crpt_dao.get_by_id(crpt_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Crpt dump with id {crpt_id} not found",
            )

        return Crpt.model_validate(result)

    async def get_by_qr_code(self, qr_code: str) -> Crpt:
        result = await self.crpt_dao.get_by_qr_code(qr_code)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Crpt dump with qr code {qr_code} not found",
            )

        return Crpt.model_validate(result)

    async def get_count(self) -> Count:
        result = await self.crpt_dao.get_count()
        return Count(total=result)

    async def get_from_crpt_api(self, fiscal_fields: FiscalFields) -> dict[str, Any]:
        client_kwargs = {
            "timeout": settings.timeout_seconds,
            "headers": {
                "content-type": "application/json",
                "accept": "application/json",
                "user-agent": (
                    "Platform: iOS 17.2; "
                    "AppVersion: 4.47.0; "
                    "AppVersionCode: 7630; "
                    "Device: iPhone 14 Pro;"
                ),
                "client": "iOS 17.2; AppVersion: 4.47.0; Device: iPhone 14 Pro;",
            },
        }

        try:
            async with AsyncClient(**client_kwargs) as crpt_client:
                response = await crpt_client.post(
                    "https://mobile.api.crpt.ru/mobile/check",
                    json={"code": fiscal_fields.qr_code, "codeType": "qr"},
                )
                response.raise_for_status()
                response = response.json()

                if not response.get("codeFounded"):
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Crpt was not found by qr code",
                    )

                return response

        except TimeoutException:
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="Cannot reach the CRPT API by timeout",
            )

        except ConnectError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="No internet connection",
            )

    @transactional
    async def create(self, dump: dict[str, Any]) -> Crpt:
        result = await self.crpt_dao.get_by_qr_code(dump["code"])
        if not result:
            result = await self.crpt_dao.create(dump)

        return Crpt.model_validate(result)

    async def delete(self, crpt_id: UUID7) -> Crpt:
        result = await self.crpt_dao.get_by_id(crpt_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Crpt with id {crpt_id} was not found",
            )

        result = self.crpt_dao.delete(result)
        return result

    async def export(self) -> StreamingResponse:
        result = await self.crpt_dao.get_qr_codes()
        total = len(result)

        async def generate():
            yield '{\n\t"qr_codes": [\n\t\t'
            first = True
            for code in result:
                if not first:
                    yield ",\n\t\t"
                first = False
                yield f'"{code}"'
            yield "\n\t],\n\t"
            yield f'"total": {total}'
            yield "\n}"

        return StreamingResponse(
            generate(),
            media_type="application/json",
            headers={"Content-Disposition": "attachment; filename=qr_codes_export.json"},
        )
