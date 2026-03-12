# apps/users/infrastructure/repositories/user_repository_impl.py

from typing import Optional, List
from uuid import UUID

from apps.users.interfaces.user_repository import UserRepository
from apps.users.entities.user import User as UserEntity
from apps.users.models.user import User as UserModel


class UserRepositoryImpl(UserRepository):

    def _to_entity(self, model: UserModel) -> UserEntity:
        return UserEntity(
            id=model.id,
            username=model.username,
            email=model.email,
            password_hash=model.password_hash,
            is_active=model.is_active,
            is_verified=model.is_verified,
            last_login=model.last_login,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def get_by_id(self, user_id: UUID) -> Optional[UserEntity]:

        try:
            user = UserModel.objects.get(id=user_id)
            return self._to_entity(user)
        except UserModel.DoesNotExist:
            return None

    def get_by_email(self, email: str) -> Optional[UserEntity]:

        try:
            user = UserModel.objects.get(email=email)
            return self._to_entity(user)
        except UserModel.DoesNotExist:
            return None

    def get_by_username(self, username: str) -> Optional[UserEntity]:

        try:
            user = UserModel.objects.get(username=username)
            return self._to_entity(user)
        except UserModel.DoesNotExist:
            return None

    def list(self) -> List[UserEntity]:

        users = UserModel.objects.all()

        return [self._to_entity(user) for user in users]

    def create(self, user: UserEntity) -> UserEntity:

        model = UserModel.objects.create(
            id=user.id,
            username=user.username,
            email=user.email,
            password_hash=user.password_hash,
            is_active=user.is_active,
            is_verified=user.is_verified,
        )

        return self._to_entity(model)

    def update(self, user: UserEntity) -> UserEntity:

        model = UserModel.objects.get(id=user.id)

        model.username = user.username
        model.email = user.email
        model.password_hash = user.password_hash
        model.is_active = user.is_active
        model.is_verified = user.is_verified

        model.save()

        return self._to_entity(model)

    def delete(self, user_id: UUID) -> None:

        UserModel.objects.filter(id=user_id).delete()
