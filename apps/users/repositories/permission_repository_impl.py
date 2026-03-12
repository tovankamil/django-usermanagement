# infrastructure/repositories/permission_repository_impl.py


from apps.users.interfaces.permission_repository import PermissionRepository
from apps.users.entities.permission import Permission as PermissionEntity
from apps.users.models.permissions import Permission as PermissionModel


class PermissionRepositoryImpl(PermissionRepository):

    def _to_entity(self, model):

        return PermissionEntity(
            id=model.id, code=model.code, name=model.name, description=model.description
        )

    def get_by_id(self, permission_id: int):

        try:
            permission = PermissionModel.objects.get(id=permission_id)
            return self._to_entity(permission)
        except PermissionModel.DoesNotExist:
            return None

    def get_by_code(self, code: str):

        try:
            permission = PermissionModel.objects.get(code=code)
            return self._to_entity(permission)
        except PermissionModel.DoesNotExist:
            return None

    def list(self):

        permissions = PermissionModel.objects.all()

        return [self._to_entity(p) for p in permissions]

    def create(self, permission: PermissionEntity):

        model = PermissionModel.objects.create(
            code=permission.code,
            name=permission.name,
            description=permission.description,
        )

        return self._to_entity(model)
