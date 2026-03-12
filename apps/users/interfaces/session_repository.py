# apps/users/domain/repositories/session_repository.py

from abc import ABC, abstractmethod
from typing import List
from uuid import UUID
from apps.users.domain.entities.session import Session


class SessionRepository(ABC):

    @abstractmethod
    def create(self, session: Session) -> Session:
        pass

    @abstractmethod
    def get_user_sessions(self, user_id: UUID) -> List[Session]:
        pass

    @abstractmethod
    def revoke(self, session_token: str) -> None:
        pass
