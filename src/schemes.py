from pydantic import BaseModel


class QRCodeRequest(BaseModel):
    qr_code: str


class ReceiptResponse(BaseModel):
    success: bool
    data: dict | None
    error: str | None
    receipt_id: str | None
