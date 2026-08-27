from decimal import Decimal

from pydantic import UUID7, BaseModel, ConfigDict, Field


class ItemId(BaseModel):
    item_id: UUID7 = Field(
        example="UUID",
        description="Unique identifier for the item",
    )


class Item(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID7 = Field(
        example="UUID",
        description="Unique identifier for the item",
    )
    receipt_id: UUID7 = Field(
        example="UUID",
        description="Link to receipt containing this item",
    )
    name: str | None = Field(
        example="Хлеб",
        description="Item name",
    )
    price: Decimal = Field(
        example=Decimal("10.50"),
        description="Price for exactly one measure of item",
    )
    total: Decimal = Field(
        example=Decimal("21.00"),
        description="Total price of items bought, should be equal to quantity times price",
    )
    quantity: float = Field(
        example=2.0,
        description="Number of items bought",
    )
    measure: int = Field(
        example=1,
        description="Type of measure for bought item (ID from measures_orm)",
    )
    nds: int = Field(
        example=1,
        description="Type of VAT (НДС) for item (ID from nds_orm)",
    )
    payment: int = Field(
        example=1,
        description="Item payment type (ID from payments_orm)",
    )
    product: int = Field(
        example=1,
        description="Product category (ID from products_orm)",
    )


class ItemList(BaseModel):
    items: list[Item]
