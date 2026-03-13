# apps/users/tests/conftest.py
import pytest
import os
import django

# Pastikan Django settings sudah setup sebelum import model
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project.settings")
django.setup()

from unittest.mock import Mock
from uuid import uuid4, UUID
from datetime import datetime

from apps.users.entities.user import User
from apps.users.repositories.user_repository_impl import UserRepository
from apps.users.services.user_service_impl import UserServiceImpl


@pytest.fixture
def mock_user_repository():
    """Mock repository - no database needed."""
    return Mock(spec=UserRepository)


@pytest.fixture
def user_service(mock_user_repository):
    """Service with mocked repository."""
    return UserServiceImpl(user_repository=mock_user_repository)


@pytest.fixture
def sample_user():
    """Sample user entity."""
    return User(
        id=uuid4(),
        username="johndoe",
        email="john@example.com",
        password_hash="hashed_password_123",
        is_active=True,
        is_verified=False,
        last_login=None,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


@pytest.fixture
def another_user():
    """Fixture for another User entity (for conflict testing)."""
    return User(
        id=uuid4(),
        username="janedoe",
        email="jane@example.com",
        password_hash="hashed_password_456",
        is_active=True,
        is_verified=True,
        last_login=datetime.now(),
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
