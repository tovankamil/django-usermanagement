import uuid
from datetime import datetime
from django.test import SimpleTestCase
from apps.users.entities.user import User


class TestUserEntity(SimpleTestCase):

    def setUp(self):
        self.valid_user_data = {
            "id": uuid.uuid4(),
            "username": "Developer Pro from indonesia",
            "email": "tovan.kamil@gmail.com",
            "password_hash": "pvasdaseed",
            "is_active": True,
            "is_verified": False,
            "last_login": None,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }

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

    def test_create_user_entity_success(self):
        """Test to create user properly"""

        user = User(**self.valid_user_data)
        self.assertEqual(user.username, self.valid_user_data["username"])
        self.assertEqual(user.email, self.valid_user_data["email"])
        self.assertIsInstance(user.id, uuid.UUID)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_verified)

    def test_create_user_entity_missing_fields(self):
        """Data class  throw error if the field not full fill"""

        invalid_data = {"username": "incompleted user"}

        with self.assertRaises(TypeError):
            User(**invalid_data)

    def test_user_entity_invalid_type(self):
        user = User(**{**self.valid_user_data, "username": None})
        self.assertIsNone(user.username)
