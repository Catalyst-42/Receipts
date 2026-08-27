from datetime import datetime
from decimal import Decimal
from typing import Any

from pydantic import (
    UUID7,
    BaseModel,
    Field,
    computed_field,
    field_validator,
    ConfigDict,
)


class ReceiptId(BaseModel):
    receipt_id: UUID7 = Field(
        example="019f9835-fcb5-7263-99e7-4cdf4146abb1",
        description="Unique id of scanned receipt",
    )


class FiscalFields(BaseModel):
    t: str = Field(
        example="20231203T2319",
        description="Receipt timestamp",
        validate_default=True,
    )
    s: Decimal = Field(
        example="261.80",
        description="Total amount",
        max_digits=15,
        decimal_places=2,
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

    @classmethod
    def _parse_fiscal_time(cls, value: Any) -> datetime:
        """Tries to parse fiscal time by two formats"""
        time_formats = ("%Y%m%dT%H%M", "%Y%m%dT%H%M%S")

        for time_format in time_formats:
            try:
                return datetime.strptime(value, time_format).replace(tzinfo=None)
            except ValueError:
                continue

        raise ValueError(f"Time must match format {' or '.join(time_formats)}")

    @field_validator("t", mode="before")
    @classmethod
    def validate_fiscal_time(cls, value: Any) -> Any:
        """Validates fiscal time date and time format"""
        cls._parse_fiscal_time(value)
        return value

    @computed_field
    @property
    def t_datetime(self) -> datetime:
        """Returns fiscal time as datetime object"""
        return self._parse_fiscal_time(self.t)

    @computed_field
    @property
    def qr_code(self) -> str:
        """Returns fiscal fields in URL format stored in QR code"""
        parts = [
            f"t={self.t}",
            f"s={self.s:.2f}",
            f"fn={self.fn}",
            f"i={self.i}",
            f"fp={self.fp}",
            f"n={self.n}",
        ]

        return "&".join(parts)


class Receipt(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID7 = Field(
        example="019f9835-fcb5-7263-99e7-4cdf4146abb1",
        description="Unique id of scanned receipt",
    )
    crpt_id: UUID7 | None = Field(
        default=None,
        example="019f9835-fcb5-7263-99e7-4cdf4146abb1",
        description="Reference to the original CRPT record",
    )
    shop_id: UUID7 | None = Field(
        default=None,
        example="019f9835-fcb5-7263-99e7-4cdf4146abb1",
        description="Reference to the shop where receipt was made",
    )
    employee_id: UUID7 | None = Field(
        default=None,
        example="019f9835-fcb5-7263-99e7-4cdf4146abb1",
        description="Reference to the employee who made this receipt",
    )

    t: datetime = Field(
        # example="20231203T2319",
        description="Receipt timestamp",
        validate_default=True,
    )
    s: Decimal = Field(
        example="261.80",
        description="Total amount",
        max_digits=15,
        decimal_places=2,
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


class ReceiptList(BaseModel):
    items: list[Receipt]
