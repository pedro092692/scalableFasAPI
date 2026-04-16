from sqlalchemy.orm import Session
from app.models.user import UserModel
from app.schemas.user import UserCreate, UserUpdate
from typing import Optional


class UserRepository:
    """
    this layer manage the data
    """

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> Optional[UserModel]:
        """
        Searches for user in the database by its unique ID.

        Args:
            user_id (int): The user ID identifier

        Returns:
            Optional[UserModel]: The user object if it exists otherwise none
        """
        return self.db.query(UserModel).filter(
            UserModel.id == user_id
        ).first()

    def get_by_email(self, user_email) -> UserModel | None:
        """
        Searches for user in the database by its email
        :param user_email: The user email identifier
        :return: Optional[UserModel]: The user object if it exits otherwise None
        """
        return self.db.query(UserModel).filter(
            UserModel.email == user_email
        ).first()

    def get_all(self, skip: int = 0, limit: int = 10) -> list[UserModel]:
        """
        List all user in the database
        :param skip: the number of skip results
        :param limit: the number of returned results
        :return: list with databse results
        """
        users = self.db.query(UserModel).offset(skip).limit(limit).scalar().all()
        print(users)
        return self.db.query(UserModel).offset(skip).limit(limit).scalar().all()

    def create(self, data: UserCreate,) -> UserModel:
        """
        Creates a new user in the database
        :param data: user data name, email and password
        :return: the new user created Usermodel
        """
        user = UserModel(
            name=data.name,
            email=data.email,
            password=data.password
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user: UserModel, data: UserUpdate) -> UserModel:
        """
        Update a user with new data
        :param user: the user object to be edited
        :param data: the new data for example name or user email
        :return: user model object with new update data
        """
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(user, field, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user: UserModel) -> None:
        self.db.delete(user)
        self.db.commit()
        return None