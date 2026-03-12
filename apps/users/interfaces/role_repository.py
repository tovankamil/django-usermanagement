# apps/users/domain/repositories/role_repository.py

from abc import ABC, abstractmethod
from typing import List, Optional
from apps.users.entities.role import Role


class RoleRepository(ABC):

    @abstractmethod
    def get_by_id(self, role_id: int) -> Optional[Role]:
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> Optional[Role]:
        pass

    @abstractmethod
    def list(self) -> List[Role]:
        pass

    @abstractmethod
    def create(self, role: Role) -> Role:
        pass

    @abstractmethod
    def delete(self, role_id: int) -> None:
        pass
