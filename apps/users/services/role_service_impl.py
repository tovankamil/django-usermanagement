from typing import List

from apps.users.interfaces.role_service import RoleService
from apps.users.entities.role import Role
from apps.users.repositories.role_repository_impl import RoleRepository


class RoleServiceImpl(RoleService):

    def __init__(self, role_repository: RoleRepository):
        self.role_repository = role_repository

    def create_role(self, name: str, description: str) -> Role:

        role = Role(id=None, name=name, description=description, created_at=None)

        return self.role_repository.create(role)

    def assign_role(self, user_id, role_id) -> None:

        # biasanya akan insert ke table user_roles
        # tergantung repository design
        pass

    def get_user_roles(self, user_id) -> List[Role]:

        # implementasi tergantung relation repository
        return []
