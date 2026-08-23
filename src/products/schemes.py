from pydantic import BaseModel, ConfigDict, Field


class GetProductByIdRequest(BaseModel):
    product_id: int = Field(
        example=5,
        description="Unique identifier of the product type",
    )

class Product(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(
        example=5,
        description="Unique identifier of the product type",
    )
    description: str = Field(
        example="О приеме ставок при осуществлении деятельности по проведению азартных игр",
        description="Full measure description",
    )
    pf_format: str = Field(
        example="СТАВКА АЗАРТНОЙ ИГРЫ",
        description="Short code for print format of product type",
    )


class ProductList(BaseModel):
    items: list[Product]
