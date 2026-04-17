from app.repositories.user_repo import UserRepository
from app.schemas.user import UserCreate, UserUpdate, UserResponse, PaginatedUser
from fastapi import HTTPException, status
import logging

logger = logging.getLogger(__name__)


class UserService:
    """
    Business logic manages repositories
    Don't know  HTTP or SQL
    """
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def create_user(self, data: UserCreate) -> UserResponse:
        logger.info(f'Creando usuario: {data.email}')
        # rule unique email
        if self.repo.get_by_email(data.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f'El email: {data.email} ya esta registrado'
            )
        user = self.repo.create(data)
        logger.info(f'Usuario creado con ID: {user.id}')
        return UserResponse.model_validate(user)

    def get_user_or_404(self, user_id: int) -> UserResponse:
        user = self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Usuario con ID {user_id} no encontrado'
            )
        return UserResponse.model_validate(user)

    def update_user(self, user_id: int, data: UserUpdate) -> UserResponse:
        user = self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Usuario con ID {user_id} no encontrado'
            )
        updated = self.repo.update(user, data)
        return UserResponse.model_validate(updated)

    def delete_user(self, user_id: int) -> None:
        logger.info(f'Eliminando usario con el ID: {user_id}')
        user = self.repo.get_by_id(user_id)
        if not user:
            logger.info(f'Con el ID: {user_id} No eliminado (no Existe)')
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Usuario con ID {user_id} no encontrado'
            )
        logger.info(f'Usuario con el ID: {user_id} eliminado...')
        return self.repo.delete(user)

    def all_users(self, page: int = 1, limit: int = 10) -> PaginatedUser:
        offset = (page - 1) * limit
        users = self.repo.get_all(skip=offset, limit=limit)
        total_users = self.repo.count_all()

        return PaginatedUser(
            items=users,
            total=total_users,
            page=page,
            per_page=limit
        )


