# users/domain/entities/session.py

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Session:
    id: int
    user_id: UUID
    session_token: str
    ip_address: str
    user_agent: str
    expires_at: datetime
    is_revoked: bool
    created_at: datetime
