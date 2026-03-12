import uuid
from django.test import SimpleTestCase
from apps.users.entities.user import User
from .mock_user_repository import MockUserRepository


class TestUserRepository(SimpleTestCase):

    def setUp(self):
        self.repo = MockUserRepository()

    def test_create_user(self):

        user = User(
            id=uuid.uuid4(),
            username="john",
            email="john@mail.com",
            password_hash="hash",
            is_active=True,
            is_verified=False,
            last_login=None,
            created_at=None,
            updated_at=None,
        )

        created = self.repo.create(user)

        self.assertEqual(created.username, "john")

    def test_get_user_by_email(self):

        user = User(
            id=uuid.uuid4(),
            username="jane",
            email="jane@mail.com",
            password_hash="hash",
            is_active=True,
            is_verified=False,
            last_login=None,
            created_at=None,
            updated_at=None,
        )

        self.repo.create(user)

        result = self.repo.get_by_email("jane@mail.com")

        self.assertEqual(result.username, "jane")

    def test_delete_user(self):

        user = User(
            id=uuid.uuid4(),
            username="delete_me",
            email="delete@mail.com",
            password_hash="hash",
            is_active=True,
            is_verified=False,
            last_login=None,
            created_at=None,
            updated_at=None,
        )

        self.repo.create(user)

        self.repo.delete(user.id)

        result = self.repo.get_by_id(user.id)

        self.assertIsNone(result)
