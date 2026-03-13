from abc import ABC, abstractmethod
from uuid import UUID
from typing import List

from apps.users.entities.session import Session


class SessionService(ABC):

    @abstractmethod
    def create_session(self, session: Session) -> Session:
        pass

    @abstractmethod
    def get_user_sessions(self, user_id: UUID) -> List[Session]:
        pass

    @abstractmethod
    def revoke_session(self, session_token: str) -> None:
        pass
