from sqlalchemy.orm import Session
from app.database import LocalSession
from app.repositories.user_repo import UserRepository
from app.services.user_service import UserService
from fastapi import Depends


def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    repo = UserRepository(db)
    return UserService(repo)
