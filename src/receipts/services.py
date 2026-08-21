from fastapi.responses import StreamingResponse
from pydantic import UUID7
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException, status
from src.config import settings
from src.core.crpt import Crpt
from src.receipts.dao import ReceiptsDao
from src.receipts.schemes import (
    GetReceiptByFiscalDataRequest,
    ReceiptData,
    ReceiptsCount,
    TotalSum,
    ReceiptListResponse,
    ReceiptData,
)


class ReceiptService:
    def __init__(self, db: AsyncSession):
        self.receipts_dao = ReceiptsDao(db)

    async def get_receipt_count(self) -> ReceiptsCount:
        """Returns total number of rows in receipts table"""
        count = await self.receipts_dao.get_receipt_count()
        return ReceiptsCount(count=count)

    async def get_receipt_total_sum(self) -> TotalSum:
        """Returns total sum of all collected receipts"""
        total_sum = await self.receipts_dao.get_receipt_total_sum()
        return TotalSum(total_sum=total_sum)

    async def get_receipt_by_id(self, receipt_id: UUID7) -> ReceiptData:
        """Returns receipt response by its UUID"""
        receipt = await self.receipts_dao.get_receipt_by_id(receipt_id)
        if not receipt:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Receipt was not found by fiscal data",
            )

        return ReceiptData(
            receipt_id=receipt.id,
            data=receipt.crpt_data,
        )

    async def get_receipt_by_fiscal_data(
        self, fiscal_data: GetReceiptByFiscalDataRequest
    ) -> ReceiptData:
        """Tries to find receipt locally or in CRPT"""
        existing_receipt = await self.receipts_dao.get_receipt_by_fiscal_data(
            t=fiscal_data.t_datetime,
            s=fiscal_data.s,
            fn=fiscal_data.fn,
            i=fiscal_data.i,
            fp=fiscal_data.fp,
            n=fiscal_data.n,
        )

        if existing_receipt:
            return ReceiptData(
                receipt_id=existing_receipt.id,
                data=existing_receipt.crpt_data,
            )

        # Try to ask CRPT
        qr_parts = [
            f"t={fiscal_data.t}",
            f"s={fiscal_data.s:.2f}",
            f"fn={fiscal_data.fn}",
            f"i={fiscal_data.i}",
            f"fp={fiscal_data.fp}",
            f"n={fiscal_data.n}",
        ]
        qr_code = "&".join(qr_parts)

        # Call external API with formed QR code
        try:
            crpt = Crpt(settings.proxy)
            crpt_data = crpt.infoFromReceipt(qr_code)

        except Exception:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="CRPT API not available",
            )

        if crpt_data.get("codeFounded"):
            receipt = await self.receipts_dao.create_receipt(crpt_data)
            return ReceiptData(
                receipt_id=receipt.id,
                data=crpt_data,
            )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Receipt was not found by fiscal data",
        )

    async def get_json_dump(self) -> StreamingResponse:
        receipts = await self.receipts_dao.get_receipts_all()

        async def generate():
            yield "["
            first = True
            for receipt in receipts:
                if not first:
                    yield ","
                first = False
                data = ReceiptData(receipt_id=receipt.id, data=receipt.crpt_data)
                yield data.model_dump_json()
            yield "]"

        return StreamingResponse(
            generate(),
            media_type="application/json",
            headers={"Content-Disposition": "attachment; filename=receipts.json"},
        )
