# apps/users/infrastructure/repositories/user_repository_impl.py

from typing import Optional, List
from uuid import UUID
import logging

from django.db import DatabaseError, IntegrityError, OperationalError
from apps.users.interfaces.user_repository import UserRepository
from apps.users.entities.user import User as UserEntity
from apps.users.models.user import User as UserModel
from ..exceptions.exceptions import (
    DatabaseException,
    NotFoundException,
    DuplicateEntryException,
)

logger = logging.getLogger(__name__)


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
        except (DatabaseError, OperationalError) as e:
            logger.error(f"Database error when get_by_id {user_id}:{str(e)}")
            raise DatabaseException(f"failed to get id: {str(e)}") from e

    def get_by_email(self, email: str) -> Optional[UserEntity]:

        try:
            user = UserModel.objects.get(email=email)
            return self._to_entity(user)
        except UserModel.DoesNotExist:
            return None
        except (DatabaseError, OperationalError) as e:
            logger.error(f"Database error when get_by_email {email}:{str(e)}")
            raise DatabaseException(f"failed to get data: {str(e)}") from e

    def get_by_username(self, username: str) -> Optional[UserEntity]:

        try:
            user = UserModel.objects.get(username=username)
            return self._to_entity(user)
        except UserModel.DoesNotExist:
            return None
        except (DatabaseError, OperationalError) as e:
            logger.error(f"Database error when get_by_username {username}:{str(e)}")
            raise DatabaseException(f"failed to get data: {str(e)}") from e

    def list(self) -> List[UserEntity]:
        try:
            users = UserModel.objects.all()
            return [self._to_entity(user) for user in users]
        except (DatabaseError, OperationalError) as e:
            logger.error(f"Database error saat list users: {str(e)}")
            raise DatabaseException(f"Gagal mengambil daftar user: {str(e)}") from e

    def create(self, user: UserEntity) -> UserEntity:
        try:
            model = UserModel.objects.create(
                id=user.id,
                username=user.username,
                email=user.email,
                password_hash=user.password_hash,
                is_active=user.is_active,
                is_verified=user.is_verified,
            )

            return self._to_entity(model)
        except IntegrityError as e:
            logger.error(f"Integrity error on create user: {str(e)}")
            raise DuplicateEntryException(f"User already exists: {str(e)}") from e
        except (DatabaseError, OperationalError) as e:
            logger.error(f"Database error on create user: {str(e)}")
            raise DatabaseException(f"failed create user: {str(e)}") from e

    def update(self, user: UserEntity) -> UserEntity:

        try:
            model = UserModel.objects.get(id=user.id)

            model.username = user.username
            model.email = user.email
            model.password_hash = user.password_hash
            model.is_active = user.is_active
            model.is_verified = user.is_verified

            model.save()

            return self._to_entity(model)
        except UserModel.DoesNotExist:
            logger.error(f"User tidak ditemukan saat update: {user.id}")
            raise NotFoundException(f"User dengan ID {user.id} tidak ditemukan")
        except IntegrityError as e:
            logger.error(f"Integrity error saat update user {user.id}: {str(e)}")
            raise DuplicateEntryException(f"Data conflict saat update: {str(e)}") from e
        except (DatabaseError, OperationalError) as e:
            logger.error(f"Database error saat update user {user.id}: {str(e)}")
            raise DatabaseException(f"Gagal update user: {str(e)}") from e

    def delete(self, user_id: UUID) -> None:

        try:
            deleted_count, _ = UserModel.objects.filter(id=user_id).delete()
            if deleted_count == 0:
                logger.warning(f"User not found: {user_id}")
        except (DatabaseError, OperationalError) as e:
            logger.error(f"Database error on deleted user {user_id}: {str(e)}")
            raise DatabaseException(f"failed deleting user: {str(e)}") from e
