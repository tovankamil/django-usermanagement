# apps/users/domain/repositories/activity_log_repository.py

from abc import ABC, abstractmethod
from typing import List
from uuid import UUID
from apps.users.domain.entities.activity_log import ActivityLog


class ActivityLogRepository(ABC):

    @abstractmethod
    def create(self, log: ActivityLog) -> ActivityLog:
        pass

    @abstractmethod
    def list_by_user(self, user_id: UUID) -> List[ActivityLog]:
        pass
