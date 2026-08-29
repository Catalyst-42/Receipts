from pydantic import UUID7, BaseModel, ConfigDict, Field


class EmployeeId(BaseModel):
    employee_id: UUID7 = Field(
        example="01a04f1b-cb71-7123-b575-91edea76f251",
        description="Unique identifier for the employee",
    )


class Employee(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID7 = Field(
        example="01a04f1b-cb71-7123-b575-91edea76f251",
        description="Unique identifier for the employee",
    )
    shop_id: UUID7 = Field(
        example="01a04f1b-cb6e-7369-8c90-95f53acfe703",
        description="Link to shops where this employee works",
    )
    name: str = Field(
        example="Самообслуживание 2",
        description="Operator name",
    )


class EmployeeList(BaseModel):
    items: list[Employee]
