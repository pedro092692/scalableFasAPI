from app.repositories.user_repo_mongo import UserMongoRepository
from app.schemas.user import UserCreate, UserMongoResponse
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)


class UserMongoService:

    def __init__(self, repo: UserMongoRepository):
        self.repo = repo

    async def create_user(self, data: UserCreate) -> UserMongoResponse:
        if await self.repo.get_by_email(data.email):
            raise HTTPException(409, 'Esta email ya esta registrado')
        user = await self.repo.create(data.name, data.email, data.password)
        logger.info(f'Usuario en mongoDB creado: {user.id}')

        return UserMongoResponse(
            id=str(user.id),
            name=user.name,
            email=user.email
        )