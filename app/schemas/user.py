from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Optional


# Request schema (that api receives)
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

    @field_validator('name')
    @classmethod
    def name_must_not_be_empty(cls, v: str):
        if not v.strip():
            raise ValueError('El nombre no puede estar vacio')
        return v.strip()


    @field_validator('password')
    @classmethod
    def password_min_lengts(cls, v: str):
        if len(v) < 8:
            raise ValueError('La contraseña debe tener al menos 8 caracteres')
        return v


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None


# Response schema (that apis returns)
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    # created_at: datetime

    model_config = {'from_attributes': True}


# Schema for pagination
class PaginatedUser(BaseModel):
    items: list[UserResponse]
    total: int
    page: int
    per_page: int

