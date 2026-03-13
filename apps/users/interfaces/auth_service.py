from abc import ABC, abstractmethod
from typing import Optional

from apps.users.entities.user import User


class AuthService(ABC):

    @abstractmethod
    def register(self, username: str, email: str, password: str) -> User:
        pass

    @abstractmethod
    def login(self, email: str, password: str) -> Optional[User]:
        pass

    @abstractmethod
    def logout(self, session_token: str) -> None:
        pass
