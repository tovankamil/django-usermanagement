# users/domain/entities/user_role.py

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class UserRole:
    id: int
    user_id: UUID
    role_id: int
    assigned_at: datetime
