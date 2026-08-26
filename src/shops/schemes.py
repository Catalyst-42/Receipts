from pydantic import UUID7, BaseModel, ConfigDict, Field


class ShopId(BaseModel):
    retailer_id: UUID7 = Field(
        example="019f9835-fcb5-7263-99e7-4cdf4146abb1",
        description="Link on retailer - owner of this shop",
    )


class Shop(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID7 = Field(
        example="019f9835-fcb5-7263-99e7-4cdf4146abb1",
        description="Unique identifier of the retailer",
    )
    retailer_id: UUID7 = Field(
        example="019f9835-fcb5-7263-99e7-4cdf4146abb1",
        description="Link on retailer - owner of this shop",
    )
    address: str | None = Field(
        example="109316, Москва, Волгоградский проспект, 42, к 9",
        description="Physical address of a shop. Null if shop is online one",
    )


class ShopList(BaseModel):
    items: list[Shop]
