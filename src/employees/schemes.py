from pydantic import UUID7, BaseModel, ConfigDict, Field


class EmployeeId(BaseModel):
    employee_id: UUID7 = Field(
        example="",
        description="Unique identifier for the employee",
    )


class Employee(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID7 = Field(
        example="",
        description="Unique identifier for the employee",
    )
    shop_id: UUID7 = Field(
        example="",
        description="Link to shops where this employee works",
    )
    name: str = Field(
        example="Тбайт",
        description="Employee name",
    )


class EmployeeList(BaseModel):
    items: list[Employee]
