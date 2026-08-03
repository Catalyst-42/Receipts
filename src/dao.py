from typing import Optional
from uuid import uuid7

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

    async def get_receipt_count(self) -> int:
        """Returns total numer of rows of receipts table"""
        stmt = select(func.count()).select_from(ReceiptsOrm)
        result = await self.db.execute(stmt)
        return result.scalar()

    async def create_receipt(self, qr_code: str, receipt_data: dict) -> ReceiptsOrm:
        """Creates new record in receipts table"""
        stmt = ReceiptsOrm(
            id=str(uuid7()),
            qr_code=qr_code,
            receipt_data=receipt_data,
        )

        self.db.add(stmt)
        await self.db.commit()
        return stmt
