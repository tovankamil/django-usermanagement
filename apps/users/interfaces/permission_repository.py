# apps/users/domain/repositories/permission_repository.py

from abc import ABC, abstractmethod
from typing import List, Optional
from apps.users.domain.entities.permission import Permission


class PermissionRepository(ABC):

    @abstractmethod
    def get_by_id(self, permission_id: int) -> Optional[Permission]:
        pass

    @abstractmethod
    def get_by_code(self, code: str) -> Optional[Permission]:
        pass

    @abstractmethod
    def list(self) -> List[Permission]:
        pass

    @abstractmethod
    def create(self, permission: Permission) -> Permission:
        pass
