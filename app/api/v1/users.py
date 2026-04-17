from fastapi import APIRouter, Depends, status
from app.schemas.user import UserCreate, UserUpdate, UserResponse, PaginatedUser
from app.services.user_service import UserService
from app.dependencies import get_user_service

router = APIRouter(prefix='/users', tags=['Users'])

@router.get('/')
def user_routes():
    return {'message': 'user routes :p'}


@router.get('/all', response_model=PaginatedUser)
async def all_users(
        page: int = 1,
        limit: int = 10,
        service: UserService = Depends(get_user_service)):
    return service.all_users(page=page, limit=limit)


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


@router.patch('/{user_id}', response_model=UserResponse)
async def update_user(user_id: int, data: UserUpdate, service: UserService = Depends(get_user_service)):
    return service.update_user(user_id, data)


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, service: UserService = Depends(get_user_service)):
    return service.delete_user(user_id)

