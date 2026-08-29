from pydantic import UUID7, BaseModel, ConfigDict, Field


class ShopId(BaseModel):
    shop_id: UUID7 = Field(
        example="01a04f1b-cb6e-7369-8c90-95f53acfe703",
        description="Unique identifier of the shop",
    )


class ShopId(BaseModel):
    retailer_id: UUID7 = Field(
        example="01a04f17-5b65-729e-abdf-d20f7c3f7567",
        description="Link on retailer - owner of this shop",
    )


class Shop(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID7 = Field(
        example="01a04f1b-cb6e-7369-8c90-95f53acfe703",
        description="Unique identifier of the retailer",
    )
    retailer_id: UUID7 = Field(
        example="01a04f17-5b65-729e-abdf-d20f7c3f7567",
        description="Link on retailer - owner of this shop",
    )
    address: str | None = Field(
        example="117525, г. Москва, ул. Днепропетровская, д. 4а, стр. 1",
        description="Physical address of a shop. Null if shop is online one",
    )


class ShopList(BaseModel):
    items: list[Shop]
