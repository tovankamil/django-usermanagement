from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class User:
    id: UUID
    username: str
    email: str
    password_hash: str
    is_active: bool
    is_verified: bool
    avatar: str
    last_login: datetime | None
    created_at: datetime
    updated_at: datetime
