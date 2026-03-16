import logging
from uuid import UUID
from typing import List, Optional

from apps.users.interfaces.user_service import UserService
from apps.users.entities.user import User
from apps.users.repositories.user_repository_impl import UserRepository
from apps.users.exceptions.exceptions import (
    DatabaseException,
    NotFoundException,
    DuplicateEntryException,
    ValidationException,
    UserNotFoundException,
    EmailAlreadyExistsException,
    UsernameAlreadyExistsException,
    UserServiceException,
)

logger = logging.getLogger(__name__)


class UserServiceImpl(UserService):

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, user: User) -> User:
        """
        Creates a new user with business rules validation.
        """
        try:
            # Validate business rules before creating
            self._validate_new_user(user)

            created_user = self.user_repository.create(user)
            logger.info(f"User successfully created: {created_user.id}")
            return created_user

        except (
            ValidationException,
            EmailAlreadyExistsException,
            UsernameAlreadyExistsException,
        ):
            # ✅ Business exceptions - re-raise tanpa modifikasi
            raise

        except DuplicateEntryException as e:
            logger.warning(f"Duplicate entry when creating user: {str(e)}")
            raise EmailAlreadyExistsException(
                "Email or username already registered"
            ) from e
        except DatabaseException as e:
            logger.error(f"Database error when creating user: {str(e)}")
            raise UserServiceException(
                "Failed to create user, please try again later"
            ) from e
        except Exception as e:
            logger.error(f"Unexpected error when creating user: {str(e)}")
            raise UserServiceException("System error occurred") from e

    def get_user(self, user_id: UUID) -> User:
        """
        Retrieves a user by ID. Raises exception if not found.
        """
        try:
            user = self.user_repository.get_by_id(user_id)

            if user is None:
                logger.warning(f"User not found: {user_id}")
                raise UserNotFoundException(f"User with ID {user_id} not found")

            return user

        except DatabaseException as e:
            logger.error(f"Database error when getting user {user_id}: {str(e)}")
            raise UserServiceException("Failed to retrieve user data") from e

    def get_user_or_none(self, user_id: UUID) -> Optional[User]:
        """
        Retrieves a user by ID. Returns None if not found (safe method).
        """
        try:
            return self.user_repository.get_by_id(user_id)
        except DatabaseException as e:
            logger.error(
                f"Database error when getting user or none {user_id}: {str(e)}"
            )
            return None

    def get_user_by_email(self, email: str) -> User:
        """
        Retrieves a user by email. Raises exception if not found.
        """
        try:
            user = self.user_repository.get_by_email(email)

            if user is None:
                logger.warning(f"User with email not found: {email}")
                raise UserNotFoundException(f"User with email {email} not found")

            return user

        except DatabaseException as e:
            logger.error(f"Database error when getting user by email: {str(e)}")
            raise UserServiceException("Failed to retrieve user data") from e

    def list_users(self) -> List[User]:
        """
        Retrieves all users.
        """
        try:
            return self.user_repository.list()
        except DatabaseException as e:
            logger.error(f"Database error when listing users: {str(e)}")
            raise UserServiceException("Failed to retrieve user list") from e

    def update_user(self, user: User) -> User:
        """
        Updates a user with business rules validation.
        """
        try:
            # Validate user exists
            existing = self.user_repository.get_by_id(user.id)
            if existing is None:
                raise UserNotFoundException(f"User with ID {user.id} not found")

            # Validate business rules for update
            self._validate_update_user(user, existing)

            updated_user = self.user_repository.update(user)
            logger.info(f"User successfully updated: {updated_user.id}")
            return updated_user

        except NotFoundException as e:
            logger.warning(f"User not found when updating: {user.id}")
            raise UserNotFoundException(str(e)) from e
        except DuplicateEntryException as e:
            logger.warning(f"Duplicate entry when updating user: {str(e)}")
            raise EmailAlreadyExistsException(
                "Email or username already used by another user"
            ) from e
        except DatabaseException as e:
            logger.error(f"Database error when updating user: {str(e)}")
            raise UserServiceException(
                "Failed to update user, please try again later"
            ) from e

    def delete_user(self, user_id: UUID) -> None:
        """
        Deletes a user by ID.
        """
        try:
            # Check if user exists before deleting
            user = self.user_repository.get_by_id(user_id)
            if user is None:
                raise UserNotFoundException(f"User with ID {user_id} not found")

            self.user_repository.delete(user_id)
            logger.info(f"User successfully deleted: {user_id}")

        except UserNotFoundException:
            raise  # Re-raise directly
        except DatabaseException as e:
            logger.error(f"Database error when deleting user {user_id}: {str(e)}")
            raise UserServiceException("Failed to delete user") from e

    # ============ PRIVATE METHODS ============

    def _validate_new_user(self, user: User) -> None:
        """
        Validates business rules for new user.
        """
        if not user.email or "@" not in user.email:
            raise ValidationException("Invalid email format")

        if not user.username or len(user.username) < 3:
            raise ValidationException("Username must be at least 3 characters")

        if not user.password_hash:
            raise ValidationException("Password is required")

        # Check if email is already registered
        existing_email = self.user_repository.get_by_email(user.email)
        if existing_email is not None:
            raise EmailAlreadyExistsException(
                f"Email {user.email} is already registered"
            )

        # Check if username is already registered
        existing_username = self.user_repository.get_by_username(user.username)
        if existing_username is not None:
            raise UsernameAlreadyExistsException(
                f"Username {user.username} is already registered"
            )

    def _validate_update_user(self, user: User, existing: User) -> None:
        """
        Validates business rules for updating user.
        """
        if not user.email or "@" not in user.email:
            raise ValidationException("Invalid email format")

        if not user.username or len(user.username) < 3:
            raise ValidationException("Username must be at least 3 characters")

        # Check if email is already used by another user
        if user.email != existing.email:
            email_check = self.user_repository.get_by_email(user.email)
            if email_check is not None and email_check.id != user.id:
                raise EmailAlreadyExistsException(
                    f"Email {user.email} is already used by another user"
                )

        # Check if username is already used by another user
        if user.username != existing.username:
            username_check = self.user_repository.get_by_username(user.username)
            if username_check is not None and username_check.id != user.id:
                raise UsernameAlreadyExistsException(
                    f"Username {user.username} is already used by another user"
                )
