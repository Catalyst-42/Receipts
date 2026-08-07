from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.core.crpt import Crpt
from src.dao import ReceiptsDao
from src.schemes import CountResponse, ReceiptResponse
from pydantic import UUID7


class ReceiptService:
    def __init__(self, db: AsyncSession):
        self.receipts_dao = ReceiptsDao(db)

    async def get_receipt_count(self) -> CountResponse:
        """Returns total numer of rows of receipts table"""
        count = await self.receipts_dao.get_receipt_count()
        return CountResponse(count=count)

    async def get_receipt_by_id(self, receipt_id: UUID7) -> ReceiptResponse:
        """Returns receipt response by its UUID"""
        receipt = await self.receipts_dao.get_receipt_by_id(receipt_id)
        if not receipt:
            return ReceiptResponse(
                success=False, data=None, error="Receipt not found", receipt_id=None
            )

        return ReceiptResponse(
            success=True, data=receipt.receipt_data, error=None, receipt_id=receipt.id
        )

    async def scan_qr_code(self, qr_code: str) -> ReceiptResponse:
        """
        Returns processed receipt from QR code

        Tries to find a qr code data in local base, or in foreign API, otherwise returns an exception
        """
        qr_code = qr_code.strip()
        if not qr_code:
            return ReceiptResponse(
                success=False, data=None, error="QR code cannot be empty", receipt_id=""
            )

        # Return receipt if its already parsed
        existing_receipt = await self.receipts_dao.get_receipt_by_qr_code(qr_code)
        if existing_receipt:
            return ReceiptResponse(
                success=True,
                data=existing_receipt.receipt_data,
                error=None,
                receipt_id=existing_receipt.id,
            )

        # Or call to API for it
        try:
            crpt = Crpt(settings.proxy)
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
            new_receipt = await self.receipts_dao.create_receipt(qr_code, receipt_data)

            return ReceiptResponse(
                success=True, data=receipt_data, error=None, receipt_id=new_receipt.id
            )

        return ReceiptResponse(
            success=False, data=None, error="Receipt was not found", receipt_id=None
        )
