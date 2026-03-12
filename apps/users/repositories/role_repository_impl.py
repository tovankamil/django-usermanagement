# infrastructure/repositories/role_repository_impl.py

from typing import Optional, List

from apps.users.interfaces.role_repository import RoleRepository
from apps.users.entities.role import Role as RoleEntity
from apps.users.models.role import Role as RoleModel


class RoleRepositoryImpl(RoleRepository):

    def _to_entity(self, model):

        return RoleEntity(
            id=model.id,
            name=model.name,
            description=model.description,
            created_at=model.created_at,
        )

    def get_by_id(self, role_id: int) -> Optional[RoleEntity]:

        try:
            role = RoleModel.objects.get(id=role_id)
            return self._to_entity(role)
        except RoleModel.DoesNotExist:
            return None

    def get_by_name(self, name: str) -> Optional[RoleEntity]:

        try:
            role = RoleModel.objects.get(name=name)
            return self._to_entity(role)
        except RoleModel.DoesNotExist:
            return None

    def list(self) -> List[RoleEntity]:

        roles = RoleModel.objects.all()

        return [self._to_entity(role) for role in roles]

    def create(self, role: RoleEntity):

        model = RoleModel.objects.create(name=role.name, description=role.description)

        return self._to_entity(model)

    def delete(self, role_id: int):

        RoleModel.objects.filter(id=role_id).delete()
