from fastapi import APIRouter, Depends, status
from app.schemas.user import UserCreate, UserUpdate, UserResponse, PaginatedUser
from app.services.user_service import UserService
from app.dependencies import get_user_service

router = APIRouter(prefix='/users', tags=['Users'])


@router.post('/', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
        data: UserCreate,
        service: UserService = Depends(get_user_service)):
    """
    Create a new user
    :param data: new user data
    :param service: user service
    :return: UserModel
    """
    return service.create_user(data)


@router.get('/{user_id}', response_model=UserResponse)
async def get_user(user_id: int, service: UserService = Depends(get_user_service)):
    return service.get_user_or_404(user_id)


@router.patch('/{user_id', response_model=UserResponse)
async def update_user(user_id: int, data: UserUpdate, service: UserService = Depends(get_user_service)):
    return service.update_user(user_id, data)