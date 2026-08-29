from pydantic import UUID7, BaseModel, ConfigDict, Field


class RetailerId(BaseModel):
    retailer_id: UUID7 = Field(
        example="01a04f17-5b65-729e-abdf-d20f7c3f7567",
        description="Unique identifier of the retailer",
    )


class Retailer(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID7 = Field(
        example="01a04f17-5b65-729e-abdf-d20f7c3f7567",
        description="Unique identifier of the retailer",
    )
    inn: str = Field(
        example="7825706086",
        description="INN (TIN) of a company or a single persona",
        min_length=10,
        max_length=12,
    )
    is_individual: bool = Field(
        example=False,
        description="Flag is the retailer is individual one, company otherwise",
    )
    name: str = Field(
        example='ООО "Агроторг"',
        description="Name of a company or a persona",
    )


class RetailerList(BaseModel):
    items: list[Retailer]
