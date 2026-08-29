from pydantic import BaseModel, ConfigDict, Field


class PaymentId(BaseModel):
    payment_id: int = Field(
        example=3,
        description="Unique identifier of the payment type",
    )

class Payment(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(
        example=3,
        description="Unique identifier of the payment type",
    )
    description: str = Field(
        example="Аванс",
        description="Full measure description",
    )
    pf_format: str = Field(
        example="АВАНС",
        description="Short code for print format of payment type",
    )


class PaymentList(BaseModel):
    items: list[Payment]
