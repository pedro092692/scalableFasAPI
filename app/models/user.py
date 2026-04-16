from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class UserModel(Base):
    __tablename__ = 'usuarios'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(String(255))
