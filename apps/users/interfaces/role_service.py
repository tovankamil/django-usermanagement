from abc import ABC, abstractmethod
from typing import List

from apps.users.entities.role import Role


class RoleService(ABC):

    @abstractmethod
    def create_role(self, name: str, description: str) -> Role:
        pass

    @abstractmethod
    def assign_role(self, user_id, role_id) -> None:
        pass

    @abstractmethod
    def get_user_roles(self, user_id) -> List[Role]:
        pass
