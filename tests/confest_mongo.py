import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.user_service_mongo import UserMongoService

@pytest.fixture
def mock_mongo_repo():
    repo = MagicMock()
    repo.get_by_email = AsyncMock(return_value=None)
    repo.get_by_id = AsyncMock(return_value=None)
    repo.create = AsyncMock()
    return repo


@pytest.fixture()
def user_service(mock_mongo_repo):
    return UserMongoService(mock_mongo_repo)