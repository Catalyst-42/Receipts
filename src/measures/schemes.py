from pydantic import BaseModel, ConfigDict, Field


class GetMeasureByIdRequest(BaseModel):
    measure_id: int = Field(
        example=83,
        description="Unique identifier of the measure",
    )

class Measure(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(
        example=83,
        description="Unique identifier of the measure",
    )
    description: str = Field(
        example="Терабайт",
        description="Full measure description",
    )
    pf_format: str = Field(
        example="Тбайт",
        description="Short code for print format of measure type",
    )


class MeasureList(BaseModel):
    items: list[Measure]
