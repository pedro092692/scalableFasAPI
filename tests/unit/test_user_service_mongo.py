import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException
from app.services.user_service_mongo import UserMongoService
from app.schemas.user import UserCreate, UserMongoResponse


def fake_mongo_user(name='john', email='john@test.com'):
    user = MagicMock()
    user.id = '507f1f77bcf86cd799439011'  # ObjectId de Mongo
    user.name = name
    user.email = email
    return UserMongoResponse(id=user.id, name=user.name, email=user.email)


class TestCreateUserMongo:
    def setup_method(self):
        self.mock_repo = MagicMock()
        self.mock_repo.get_by_email = AsyncMock(return_value=None)
        self.mock_repo.create = AsyncMock(return_value=fake_mongo_user())
        self.service = UserMongoService(self.mock_repo)

    @pytest.mark.asyncio  # necesario para tests async
    async def test_create_user_success(self):
        data = UserCreate(name='john', email='john@test.com', password='pass123secure')
        result = await self.service.create_user(data)
        self.mock_repo.get_by_email.assert_called_once_with('john@test.com')
        assert result.email == 'john@test.com'

    @pytest.mark.asyncio
    async def test_duplicate_email_raises_409(self):
        self.mock_repo.get_by_email = AsyncMock(return_value=fake_mongo_user())
        data = UserCreate(name='john', email='john@test.com', password='pass123secure')
        with pytest.raises(HTTPException) as exc_info:
            await self.service.create_user(data)
        assert exc_info.value.status_code == 409
        self.mock_repo.create.assert_not_called()