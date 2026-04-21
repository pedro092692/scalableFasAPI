import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserUpdate, UserResponse


# helper to avoid repeat usercreate in each test
def make_user_data(**kwargs):
    defaults = {
        'name': 'john doe',
        'email': 'john@doe.com',
        'password': 'secure123'
    }

    return UserCreate(**{**defaults, **kwargs})


def fake_user(id=1, name='john doe', email='john@doe.com'):
    user = MagicMock()
    user.id = id
    user.name = name
    user.email = email
    return UserResponse(id=id, name=name, email=email)


class TestCreateUser:

    def setup_method(self):
        """
        This runs in each tests
        """
        self.mock_repo = MagicMock()
        self.service = UserService(self.mock_repo)

    def test_create_user_success(self):
        # arrange email not in db
        self.mock_repo.get_by_email.return_value = None
        self.mock_repo.create.return_value = fake_user()

        # act
        data = make_user_data()
        result = self.service.create_user(data)

        self.mock_repo.get_by_email.assert_called_once_with('john@doe.com')
        self.mock_repo.create.assert_called_once()

        assert result.email == 'john@doe.com'

    def test_create_user_duplicate_email_raises_409(self):
        # arrange  the email already exits
        self.mock_repo.get_by_email.return_value = fake_user()

        data = make_user_data()

        # act & assert
        with pytest.raises(HTTPException) as exc_info:
            self.service.create_user(data)

        assert exc_info.value.status_code == 409

        # check user never created
        self.mock_repo.create.assert_not_called()


class TestGetUser:

    def setup_method(self):
        self.mock_repo = MagicMock()
        self.service = UserService(self.mock_repo)

    def test_get_existing_user_returns_user(self):
        self.mock_repo.get_by_id.return_value = fake_user(id=42)

        result = self.service.get_user_or_404(42)

        self.mock_repo.get_by_id.assert_called_once_with(42)

        assert result.id == 42

    def test_get_nonexistent_user_raises_404(self):
        # Simula que la DB no encontró nada
        self.mock_repo.get_by_id.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            self.service.get_user_or_404(999)

        assert exc_info.value.status_code == 404

    def test_get_all_users_success(self):
        fake_list = [fake_user(id=0), fake_user(id=1)]
        self.mock_repo.get_all.return_value = fake_list
        self.mock_repo.count_all.return_value = 2

        result = self.service.all_users(page=1, limit=10)

        self.mock_repo.get_all.assert_called_once_with(skip=0, limit=10)
        self.mock_repo.count_all.assert_called_once()

        assert result.items == fake_list
        assert result.total == 2
        assert result.page == 1

    def test_get_all_users_empty(self):
        fake_list = []
        self.mock_repo.get_all.return_value = fake_list
        self.mock_repo.count_all.return_value = 0

        result = self.service.all_users(page=1, limit=10)

        self.mock_repo.get_all.assert_called_once_with(skip=0, limit=10)
        self.mock_repo.count_all.assert_called_once()

        assert result.items == fake_list
        assert result.total == 0
        assert result.page == 1


class TestUpdateUser:

    def setup_method(self):
        self.mock_repo = MagicMock()
        self.service = UserService(self.mock_repo)

    def test_update_existing_user(self):
        self.mock_repo.get_by_id.return_value = fake_user()
        self.mock_repo.update.return_value = fake_user(name="Nuevo Nombre")

        data = UserUpdate(name="Nuevo Nombre")
        result = self.service.update_user(1, data)

        self.mock_repo.update.assert_called_once()
        assert result.name == "Nuevo Nombre"

    def test_update_nonexistent_user_raises_404(self):
        self.mock_repo.get_by_id.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            self.service.update_user(999, UserUpdate(name="x"))

        assert exc_info.value.status_code == 404
        self.mock_repo.update.assert_not_called()

