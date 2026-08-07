from typing import Any
from datetime import datetime
from typing import Any

from pydantic import UUID7, BaseModel, Field, field_validator

class GetReceiptByIdRequest(BaseModel):
    receipt_id: UUID7 = Field(
        example="019f9835-fcb5-7263-99e7-4cdf4146abb1",
        description="Unique id of scanned receipt",
    )


class GetReceiptByFiscalDataRequest(BaseModel):
    t: str = Field(
        example="20231203T2319",
        description="Receipt timestamp",
    )
    s: float = Field(
        example=261.80,
        description="Total amount",
    )
    fn: int = Field(
        example=7281440701309134,
        description="Fiscal drive number (ФН)",
    )
    i: int = Field(
        example=10027,
        description="Fiscal document number (ФД)",
    )
    fp: int = Field(
        example=3516337491,
        description="Fiscal sign (ФП)",
    )
    n: int = Field(
        example=1,
        description="Operation type",
    )

    @field_validator("t", mode="before")
    @classmethod
    def validate_fiscal_time(cls, value: Any) -> Any:
        try:
            value = value.strip()
            datetime.strptime(value, "%Y%m%dT%H%M")
        except ValueError:
            raise ValueError("Fiscal time must be in format %Y%m%dT%H%M")

        return value

    @property
    def t_datetime(self) -> datetime:
        """Returns fiscal time as datetime object"""
        return datetime.strptime(self.t, "%Y%m%dT%H%M")


class ReceiptResponse(BaseModel):
    success: bool = Field(example=True, description="Status of a query")
    data: dict | None = Field(
        example={
            "id": 763297079,
            "codeFounded": True,
            "checkResult": True,
            "code": "t=20231203T2319&s=261.80&fn=7281440701309134&i=10027&fp=3516337491&n=1",
            "checkDate": 1785096201320,
            "category": "fiscal",
            "status": "received",
            "codeType": "qr",
            "codeResolveData": {
                "gsOne": False,
                "verified": False,
                "valid": False,
                "message": "cannot parse code. AiGroupNotSupportedException: AI group [t] is not supported",
                "rawCode": "t=20231203T2319&s=261.80&fn=7281440701309134&i=10027&fp=3516337491&n=1",
                "ais": {},
                "groups": [],
                "found": False,
                "known": False,
                "isBlocked": False,
            },
            "fiscalData": {
                "codeData": {
                    "fiscalDate": 1701645540000,
                    "operationType": 1,
                    "cost": 26180,
                    "fiscalDriveNumber": 7281440701309134,
                    "fiscalDocumentNumber": 10027,
                    "fiscalSign": 3516337491,
                },
                "receipt": {
                    "message": {"processingStatus": "COMPLETED"},
                    "cashTotalSum": 0,
                    "ecashTotalSum": 26180,
                    "fiscalDocumentNumber": 10027,
                    "items": [
                        {
                            "name": "100193831 ЧАЙ МАРОККАНСКИЙ С Г",
                            "price": 6900,
                            "quantity": 2,
                            "itemsQuantityMeasure": 0,
                            "sum": 13800,
                            "nds": 1,
                            "paymentType": 4,
                            "productType": 1,
                            "isProductMarked": False,
                        },
                        {
                            "name": "4660043858820 СЫРОК ГЛАЗИРОВАННЫЙ ",
                            "price": 5390,
                            "quantity": 1,
                            "itemsQuantityMeasure": 0,
                            "sum": 5390,
                            "nds": 2,
                            "rawProductCode": '0104660043858820215Y(k"o',
                            "gtin": "04660043858820",
                            "sernum": '5Y(k"o',
                            "paymentType": 4,
                            "productType": 33,
                            "isProductMarked": True,
                        },
                        {
                            "name": "4660043858837 СЫРОК ГЛАЗИРОВАННЫЙ ",
                            "price": 6990,
                            "quantity": 1,
                            "itemsQuantityMeasure": 0,
                            "sum": 6990,
                            "nds": 2,
                            "rawProductCode": "0104660043858837215CNOIV",
                            "gtin": "04660043858837",
                            "sernum": "5CNOIV",
                            "paymentType": 4,
                            "productType": 33,
                            "isProductMarked": True,
                        },
                    ],
                    "ofdId": "ofd5",
                    "operationType": 1,
                    "operator": "Самообслуживание 2",
                    "requestNumber": 272,
                    "retailPlaceAddress": "117525, г. Москва, ул. Днепропетровская, д. 4а, стр. 1",
                    "shiftNumber": 31,
                    "totalSum": 26180,
                    "user": 'ООО "СПАР МИДДЛ ВОЛГА"',
                    "userInn": "5258056945  ",
                    "nds10": 1125,
                    "nds18": 2300,
                },
            },
            "attributes": {
                "fiscalDate": 1701645540000,
                "operationType": 1,
                "cost": 26180,
                "fiscalDriveNumber": 7281440701309134,
                "fiscalDocumentNumber": 10027,
                "fiscalSign": 3516337491,
            },
            "wrongDocs": False,
            "statusV2": "received",
        },
        description="Receipt data",
    )
    error: str | None = Field(example=None, description="Response error state")
    receipt_id: UUID7 | None = Field(
        example="019f9835-fcb5-7263-99e7-4cdf4146abb1",
        description="Unique id of scanned receipt",
    )


class CountResponse(BaseModel):
    count: int = Field(example=42, description="Total count of receipts in database")
