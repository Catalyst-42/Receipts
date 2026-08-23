from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    detail: str = Field(
        example="Error occured",
        description="Description of an occured error",
    )
