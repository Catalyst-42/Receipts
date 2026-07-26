from uuid import uuid7
from typing import Optional

from nechestniy_znak import Crpt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import ReceiptOrm
from src.schemes import ReceiptResponse


class ReceiptService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_receipt_by_qr_code(self, qr_code: str) -> Optional[ReceiptOrm]:
        """Returns recipie from QR code data"""
        stmt = select(ReceiptOrm).where(ReceiptOrm.qr_code == qr_code)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_receipt(self, qr_code: str, receipt_data: dict) -> ReceiptOrm:
        """Returns new receipt"""
        new_receipt = ReceiptOrm(
            id=str(uuid7()), qr_code=qr_code, receipt_data=receipt_data
        )

        self.db.add(new_receipt)
        await self.db.commit()
        return new_receipt

    async def process_qr_code(self, qr_code: str) -> ReceiptResponse:
        """Returns processed receipt from QR code"""
        qr_code = qr_code.strip()
        if not qr_code:
            return ReceiptResponse(
                success=False, data=None, error="QR code cannot be empty", receipt_id=""
            )

        # Return receipt if its already parsed
        existing_receipt = await self.get_receipt_by_qr_code(qr_code)
        if existing_receipt:
            return ReceiptResponse(
                success=True,
                data=existing_receipt.receipt_data,
                error=None,
                receipt_id=existing_receipt.id,
            )

        # Or call to API for it
        try:
            crpt = Crpt()
            receipt_data = crpt.infoFromReceipt(qr_code)
        except Exception as e:
            return ReceiptResponse(
                success=False,
                data=None,
                error=f"API error: {str(e)}",
                receipt_id="",
            )

        # Retister new receipt
        if receipt_data["codeFounded"] == True:
            new_receipt = await self.create_receipt(qr_code, receipt_data)

            return ReceiptResponse(
                success=True, data=receipt_data, error=None, receipt_id=new_receipt.id
            )

        return ReceiptResponse(
            success=False, data=None, error="Receipt was not found", receipt_id=None
        )
