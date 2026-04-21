from app.models.user_mongo import UserDocument
from typing import Optional


class UserMongoRepository:

    async def get_by_id(self, user_id: str) -> Optional[UserDocument]:
        return await UserDocument.get(user_id)

    async def get_by_email(self, email: str) -> Optional | UserDocument:
        return await UserDocument.find_one({"email": email})

    async def create(self, name: str, email: str, password: str) -> UserDocument:
        user = UserDocument(name=name, email=email, password=password)
        await user.insert()
        return user

    async def delete(self, user: UserDocument) -> None:
        await user.delete()