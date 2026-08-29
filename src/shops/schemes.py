from pydantic import UUID7, BaseModel, ConfigDict, Field


class GetShopByIdRequest(BaseModel):
    shop_id: UUID7 = Field(
        example="",
        description="Unique identifier of the shop",
    )


class ShopId(BaseModel):
    retailer_id: UUID7 = Field(
        example="",
        description="Link on retailer - owner of this shop",
    )


class Shop(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID7 = Field(
        example="",
        description="Unique identifier of the retailer",
    )
    retailer_id: UUID7 = Field(
        example="",
        description="Link on retailer - owner of this shop",
    )
    address: str | None = Field(
        example="109316, Москва, Волгоградский проспект, 42, к 9",
        description="Physical address of a shop. Null if shop is online one",
    )


class ShopList(BaseModel):
    items: list[Shop]
