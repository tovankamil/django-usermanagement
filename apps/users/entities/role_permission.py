# users/domain/entities/role_permission.py

from dataclasses import dataclass


@dataclass
class RolePermission:
    id: int
    role_id: int
    permission_id: int
