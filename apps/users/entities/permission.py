# users/domain/entities/permission.py

from dataclasses import dataclass


@dataclass
class Permission:
    id: int
    code: str
    name: str
    description: str | None
