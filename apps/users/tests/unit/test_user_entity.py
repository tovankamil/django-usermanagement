import uuid
from django.test import SimpleTestCase
from apps.users.entities.user import User


class TestUserEntity(SimpleTestCase):

    def test_create_user_entity(self):

        user = User(
            id=uuid.uuid4(),
            username="testuser",
            email="test@mail.com",
            password_hash="hashed",
            is_active=True,
            is_verified=False,
            last_login=None,
            created_at=None,
            updated_at=None,
        )

        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@mail.com")
        self.assertTrue(user.is_active)
