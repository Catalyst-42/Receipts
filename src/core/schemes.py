from decimal import Decimal

from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    detail: str = Field(
        example="Error occured",
        description="Description of an occured error",
    )


class Status(BaseModel):
    system: bool = Field(
        example=True,
        description="Status of a system",
    )
    database: bool = Field(
        example=True,
        description="Status of a database",
    )


class Average(BaseModel):
    avg: Decimal = Field(
        example=Decimal("480.60"),
        description="Average value",
    )


class Count(BaseModel):
    total: int = Field(
        example=1479,
        description="Total count of itmes",
        ge=0,
    )


class CountDistinct(Count):
    selectivity: float = Field(
        example=0.5899481451934583,
        description="Fraction of unique items by size of group",
        ge=0,
        le=1,
    )


class Total(BaseModel):
    total: Decimal = Field(
        example=Decimal("1286574.34"),
        description="Total sum of prices",
    )


class Median(BaseModel):
    median: Decimal = Field(
        example=Decimal("139.45"),
        description="Median value",
    )
