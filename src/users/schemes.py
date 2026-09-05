from pydantic import UUID7, BaseModel, ConfigDict, Field


class AccessToken(BaseModel):
    access_token: str = Field(
        example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMWEwNmRkNi05Njk3LTc3MWQtOTQyMy04NDBkNDM2NDk0NWEiLCJleHAiOjE3ODkxOTkzNzh9.flJZB6sBsCNWFBHEjjt4k74h6wzJWIqSL8mnHBVlnZs",
        description="JWT access token from user account",
    )


class Register(BaseModel):
    username: str = Field(
        example="Catalyst",
        description="Unique user name for login",
        min_length=1,
        max_length=16,
        pattern=r"^[A-Za-z0-9_-]+$",
    )
    password: str = Field(
        example="********",
        description="Password from user account",
    )


class Login(BaseModel):
    username: str = Field(
        example="Catalyst",
        description="Unique user name for login",
    )
    password: str = Field(
        example="********",
        description="Password from user account",
    )


class Passwords(BaseModel):
    old_password: str = Field(
        example="********",
        description="Old user password from account",
    )
    new_password: str = Field(
        example="********",
        description="New password for user account",
    )


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID7 = Field(
        example="01a04f1b-cb73-7110-bd8b-b2eba9b49d11",
        description="Unique user identifier",
    )
    username: str = Field(
        example="Catalyst",
        description="Unique user name",
    )
    is_admin: bool = Field(
        example=False,
        description="Flag indicating if user is admin",
    )
