from pydantic import BaseModel, Field


class QRCodeRequest(BaseModel):
    qr_code: str = Field(
        example="t=20260724T1942&s=829.11&fn=3959286000682930&i=28960&fp=101010457&n=1",
        description="QR code string from receipt",
    )


class ReceiptResponse(BaseModel):
    success: bool = Field(example=True, description="Status of a query")
    data: dict | None = Field(
        example={
            "id": 761226629,
            "fiscalData": {
                "receipt": {
                    "cashTotalSum": 0,
                    "ecashTotalSum": 8499,
                    "fiscalDocumentNumber": 10521,
                    "items": [
                        {"...": "..."},
                        {
                            "name": "Батон НАРЕЗНОЙ в/с нарез. 400г",
                            "price": 8499,
                            "quantity": 1,
                            "itemsQuantityMeasure": 0,
                            "sum": 8499,
                            "nds": 2,
                            "paymentType": 4,
                            "productType": 1,
                            "isProductMarked": False,
                        },
                    ],
                },
                "...": "...",
            },
            "...": "...",
        },
        description="Receipt data",
    )
    error: str | None = Field(example=None, description="Response error state")
    receipt_id: str | None = Field(
        example="019f9835-fcb5-7263-99e7-4cdf4146abb1",
        description="Unique id of scanned receipt",
    )
