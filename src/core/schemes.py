from pydantic import BaseModel, Field
from decimal import Decimal


class ErrorResponse(BaseModel):
    detail: str = Field(
        example="Error occured",
        description="Description of an occured error",
    )


class Count(BaseModel):
    total: int = Field(
        example=42,
        description="Total count of itmes",
        ge=0,
    )

class Sum(BaseModel):
    sum: Decimal = Field(
        example=Decimal("1286574.34"),
        description="Total sum of prices",
        ge=Decimal(0),
    )
