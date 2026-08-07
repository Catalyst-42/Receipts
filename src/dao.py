from typing import Optional
from pydantic import UUID7
from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import ReceiptsOrm


class ReceiptsDao:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_receipt_by_qr_code(self, qr_code: str) -> Optional[ReceiptsOrm]:
        """Tries to find receipe in receipts table"""
        stmt = select(ReceiptsOrm).where(ReceiptsOrm.qr_code == qr_code)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_receipt_by_id(self, receipt_id: UUID7) -> Optional[ReceiptsOrm]:
        """Returns receipt by its UUID"""
        stmt = select(ReceiptsOrm).where(ReceiptsOrm.id == receipt_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_receipt_count(self) -> int:
        """Returns total numer of rows of receipts table"""
        stmt = select(func.count()).select_from(ReceiptsOrm)
        result = await self.db.execute(stmt)
        return result.scalar()

    async def create_receipt(self, qr_code: str, receipt_data: dict) -> ReceiptsOrm:
        """Creates new record in receipts table"""
        fiscal_data = receipt_data["fiscalData"]
        code_data = fiscal_data["codeData"]
        fiscal_date = code_data["fiscalDate"]

        t = datetime.fromtimestamp(fiscal_date / 1000)
        s = code_data["cost"] / 100
        fn = code_data["fiscalDriveNumber"]
        i = code_data["fiscalDocumentNumber"]
        fp = code_data["fiscalSign"]
        n = code_data["operationType"]

        stmt = ReceiptsOrm(
            qr_code=qr_code,
            receipt_data=receipt_data,
            t=t,
            s=s,
            fn=fn,
            i=i,
            fp=fp,
            n=n,
        )

        self.db.add(stmt)
        await self.db.commit()
        return stmt
