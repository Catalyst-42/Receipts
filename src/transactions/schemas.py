from decimal import Decimal

from pydantic import (
    UUID7,
    BaseModel,
    ConfigDict,
    Field,
)

from src.transactions.enums import TransactionType


class Transaction(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID7 = Field(
        example="01a09461-b7bd-772c-89b6-1f32a30698d4",
        description="Unique identifier for the transaction",
    )
    owner_id: UUID7 = Field(
        example="01a09461-4aa4-75e8-ac16-ba64b498fceb",
        description="Reference to the user who owns this transaction",
    )
    receipt_id: UUID7 | None = Field(
        default=None,
        example=None,
        description="Reference to the fiscal receipt associated with this transaction",
    )
    total: Decimal = Field(
        example=100.00,
        description="Total amount for transaction",
        max_digits=15,
        decimal_places=2,
        gt=0,
    )
    type: TransactionType = Field(
        example=TransactionType.OUTCOME,
        description="Transaction type by money flow",
    )
    note: str = Field(
        example="Ларёчный чебурек",
        description="Transaction type by money flow",
    )
