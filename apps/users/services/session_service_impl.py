from typing import List
from uuid import UUID

from apps.users.interfaces.session_service import SessionService
from apps.users.entities.session import Session
from apps.users.interfaces.session_repository import SessionRepository


class SessionServiceImpl(SessionService):

    def __init__(self, session_repository: SessionRepository):
        self.session_repository = session_repository

    def create_session(self, session: Session) -> Session:

        return self.session_repository.create(session)

    def get_user_sessions(self, user_id: UUID) -> List[Session]:

        return self.session_repository.get_user_sessions(user_id)

    def revoke_session(self, session_token: str) -> None:

        self.session_repository.revoke(session_token)
