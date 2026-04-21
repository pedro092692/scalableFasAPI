from beanie import Document, Indexed
from pydantic import EmailStr
from datetime import datetime
from typing import Optional
from pydantic import Field

class UserDocument(Document):
    """
        Document = el quivalente a Base + UserModel del SQLAlchemy.
        Benaie combina el modelo ORM y Pydantic en uno solo.
    """
    name: str
    email: Indexed(EmailStr, unique=True)  # primary key
    password: str
    created_at: datetime = Field(default_factory=datetime.now)
    is_active: bool = True

    class Settings:
        name = "users"
