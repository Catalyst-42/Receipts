from pydantic import UUID7
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.core.crpt import Crpt
from src.dao import ReceiptsDao
from src.schemes import CountResponse, GetReceiptByFiscalDataRequest, ReceiptResponse


class ReceiptService:
    def __init__(self, db: AsyncSession):
        self.receipts_dao = ReceiptsDao(db)

    async def get_receipt_count(self) -> CountResponse:
        """Returns total number of rows in receipts table"""
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

    async def get_receipt_by_fiscal_data(
        self, fiscal_data: GetReceiptByFiscalDataRequest
    ) -> ReceiptResponse:
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
            return ReceiptResponse(
                success=True,
                data=existing_receipt.receipt_data,
                error=None,
                receipt_id=existing_receipt.id,
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
            receipt_data = crpt.infoFromReceipt(qr_code)
        except Exception as e:
            return ReceiptResponse(
                success=False,
                data=None,
                error=f"API error: {str(e)}",
                receipt_id="",
            )

        if receipt_data.get("codeFounded"):
            receipt = await self.receipts_dao.create_receipt(receipt_data)
            return ReceiptResponse(
                success=True,
                data=receipt_data,
                error=None,
                receipt_id=receipt.id,
            )

        return ReceiptResponse(
            success=False,
            data=None,
            error="Receipt was not found by fiscal data",
            receipt_id=None,
        )
