from pydantic import BaseModel, ConfigDict, Field


class GetNdsByIdRequest(BaseModel):
    nds_id: int = Field(
        example=1,
        description="Unique identifier of the VAT (НДС)",
    )

class Nds(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(
        example=1,
        description="Unique identifier of the VAT (НДС)",
    )
    rate_name: str = Field(
        example="Ставка НДС 20%",
        description="Short tax rate name",
    )
    pf_format: str = Field(
        example="НДС 20%",
        description="Short string code for print format of VAT type",
    )


class NdsList(BaseModel):
    items: list[Nds]
