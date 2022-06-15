from pydantic import BaseModel, EmailStr, Field


class UserCreateEntity(BaseModel):
    name: str = Field(..., min_length=3, max_length=36)
    email: EmailStr
    password: str


class UserPatchEntity(BaseModel):
    name: str | None = Field(None, min_length=3, max_length=36)
    email: EmailStr | None
    is_active: bool | None


class UserEntity(BaseModel):
    id: str = Field(..., min_length=36, max_length=36)
    name: str = Field(..., min_length=3, max_length=36)
    email: EmailStr
    is_active: bool

    class Config:
        orm_mode = True
