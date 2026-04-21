from fastapi import APIRouter, Depends
from app.schemas.user import UserCreate, UserMongoResponse
from app.services.user_service_mongo import UserMongoService
from app.repositories.user_repo_mongo import UserMongoRepository

router = APIRouter(prefix='/mongo/users', tags=['Users MongoDB'])


def get_user_service() -> UserMongoService:
    return UserMongoService(UserMongoRepository())


@router.post('/', response_model=UserMongoResponse, status_code=201)
async def create_user(
        data: UserCreate,
        service: UserMongoService = Depends(get_user_service)
    ):
    return await service.create_user(data)
