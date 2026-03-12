# users/domain/entities/activity_log.py

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class ActivityLog:
    id: int
    user_id: UUID | None
    action: str
    resource: str
    ip_address: str
    metadata: dict | None
    created_at: datetime
