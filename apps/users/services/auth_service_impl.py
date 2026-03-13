import uuid
from typing import Optional
from django.contrib.auth.hashers import make_password, check_password

from apps.users.services.auth_service_impl import AuthService
from apps.users.entities.user import User
from apps.users.interfaces.user_repository import UserRepository


class AuthServiceImpl(AuthService):

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register(self, username: str, email: str, password: str) -> User:

        hashed_password = make_password(password)

        user = User(
            id=uuid.uuid4(),
            username=username,
            email=email,
            password_hash=hashed_password,
            is_active=True,
            is_verified=False,
            last_login=None,
            created_at=None,
            updated_at=None,
        )

        return self.user_repository.create(user)

    def login(self, email: str, password: str) -> Optional[User]:

        user = self.user_repository.get_by_email(email)

        if not user:
            return None

        if not check_password(password, user.password_hash):
            return None

        return user

    def logout(self, session_token: str) -> None:
        # biasanya logout dihandle session service
        pass
