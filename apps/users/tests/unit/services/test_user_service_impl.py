# apps/users/tests/services/test_user_service_impl.py

import pytest
from uuid import uuid4
from unittest.mock import Mock

from apps.users.entities.user import User
from apps.users.exceptions.exceptions import (
    DatabaseException,
    DuplicateEntryException,
    NotFoundException,
    ValidationException,
    UserNotFoundException,
    EmailAlreadyExistsException,
    UsernameAlreadyExistsException,
    UserServiceException,
)
from apps.users.services.user_service_impl import UserServiceImpl


class TestUserServiceImplInit:
    """Tests for UserServiceImpl initialization."""

    def test_init_with_repository(self, mock_user_repository):
        """Test successful initialization with repository."""
        service = UserServiceImpl(user_repository=mock_user_repository)
        assert service.user_repository is mock_user_repository


class TestCreateUser:
    """Tests for create_user method."""

    def test_create_user_success(self, user_service, mock_user_repository, sample_user):
        """Test successful user creation."""
        mock_user_repository.get_by_email.return_value = None
        mock_user_repository.get_by_username.return_value = None
        mock_user_repository.create.return_value = sample_user

        result = user_service.create_user(sample_user)

        assert result == sample_user
        mock_user_repository.create.assert_called_once_with(sample_user)
        mock_user_repository.get_by_email.assert_called_once_with(sample_user.email)
        mock_user_repository.get_by_username.assert_called_once_with(
            sample_user.username
        )

    def test_create_user_invalid_email_format(self, user_service, sample_user):
        """Test validation fails with invalid email format."""
        sample_user.email = "invalid-email"

        with pytest.raises(ValidationException) as exc_info:
            user_service.create_user(sample_user)

        assert "Invalid email format" in str(exc_info.value)
        assert exc_info.value.__cause__ is None

    def test_create_user_short_username(self, user_service, sample_user):
        """Test validation fails with short username."""
        sample_user.username = "ab"

        with pytest.raises(ValidationException) as exc_info:
            user_service.create_user(sample_user)

        assert "at least 3 characters" in str(exc_info.value)

    def test_create_user_missing_password(self, user_service, sample_user):
        """Test validation fails with missing password."""
        sample_user.password_hash = ""

        with pytest.raises(ValidationException) as exc_info:
            user_service.create_user(sample_user)

        assert "Password is required" in str(exc_info.value)

    def test_create_user_duplicate_email(
        self, user_service, mock_user_repository, sample_user, another_user
    ):
        """Test raises EmailAlreadyExistsException when email exists."""
        mock_user_repository.get_by_email.return_value = another_user

        with pytest.raises(EmailAlreadyExistsException) as exc_info:
            user_service.create_user(sample_user)

        assert sample_user.email in str(exc_info.value)
        mock_user_repository.create.assert_not_called()

    def test_create_user_duplicate_username(
        self, user_service, mock_user_repository, sample_user, another_user
    ):
        """Test raises UsernameAlreadyExistsException when username exists."""
        mock_user_repository.get_by_email.return_value = None
        mock_user_repository.get_by_username.return_value = another_user

        with pytest.raises(UsernameAlreadyExistsException) as exc_info:
            user_service.create_user(sample_user)

        assert sample_user.username in str(exc_info.value)
        mock_user_repository.create.assert_not_called()

    def test_create_user_database_error(
        self, user_service, mock_user_repository, sample_user
    ):
        """Test wraps DatabaseException in UserServiceException."""
        mock_user_repository.get_by_email.return_value = None
        mock_user_repository.get_by_username.return_value = None
        mock_user_repository.create.side_effect = DatabaseException("Connection failed")

        with pytest.raises(UserServiceException) as exc_info:
            user_service.create_user(sample_user)

        assert "Failed to create user" in str(exc_info.value)
        assert exc_info.value.__cause__ is not None

    def test_create_user_duplicate_entry_exception(
        self, user_service, mock_user_repository, sample_user
    ):
        """Test DuplicateEntryException translates to EmailAlreadyExistsException."""
        mock_user_repository.get_by_email.return_value = None
        mock_user_repository.get_by_username.return_value = None
        mock_user_repository.create.side_effect = DuplicateEntryException(
            "UNIQUE constraint failed"
        )

        with pytest.raises(EmailAlreadyExistsException) as exc_info:
            user_service.create_user(sample_user)

        assert "already registered" in str(exc_info.value)
        assert isinstance(exc_info.value.__cause__, DuplicateEntryException)

    def test_create_user_unexpected_error(
        self, user_service, mock_user_repository, sample_user
    ):
        """Test unexpected exceptions are wrapped in UserServiceException."""
        mock_user_repository.get_by_email.side_effect = Exception("Unexpected")

        with pytest.raises(UserServiceException) as exc_info:
            user_service.create_user(sample_user)

        assert "System error occurred" in str(exc_info.value)


class TestGetUser:
    """Tests for get_user method."""

    def test_get_user_success(self, user_service, mock_user_repository, sample_user):
        """Test successful user retrieval."""
        mock_user_repository.get_by_id.return_value = sample_user

        result = user_service.get_user(sample_user.id)

        assert result == sample_user
        mock_user_repository.get_by_id.assert_called_once_with(sample_user.id)

    def test_get_user_not_found(self, user_service, mock_user_repository, sample_user):
        """Test raises UserNotFoundException when user doesn't exist."""
        mock_user_repository.get_by_id.return_value = None

        with pytest.raises(UserNotFoundException) as exc_info:
            user_service.get_user(sample_user.id)

        assert str(sample_user.id) in str(exc_info.value)

    def test_get_user_database_error(
        self, user_service, mock_user_repository, sample_user
    ):
        """Test wraps DatabaseException in UserServiceException."""
        mock_user_repository.get_by_id.side_effect = DatabaseException("DB down")

        with pytest.raises(UserServiceException) as exc_info:
            user_service.get_user(sample_user.id)

        assert "Failed to retrieve user data" in str(exc_info.value)


class TestGetUserOrNone:
    """Tests for get_user_or_none method."""

    def test_get_user_or_none_success(
        self, user_service, mock_user_repository, sample_user
    ):
        """Test returns user when found."""
        mock_user_repository.get_by_id.return_value = sample_user

        result = user_service.get_user_or_none(sample_user.id)

        assert result == sample_user

    def test_get_user_or_none_not_found(self, user_service, mock_user_repository):
        """Test returns None when user not found."""
        mock_user_repository.get_by_id.return_value = None

        result = user_service.get_user_or_none(uuid4())

        assert result is None

    def test_get_user_or_none_database_error(
        self, user_service, mock_user_repository, sample_user
    ):
        """Test returns None on database error (graceful degradation)."""
        mock_user_repository.get_by_id.side_effect = DatabaseException("Timeout")

        result = user_service.get_user_or_none(sample_user.id)

        assert result is None


class TestGetUserByEmail:
    """Tests for get_user_by_email method."""

    def test_get_user_by_email_success(
        self, user_service, mock_user_repository, sample_user
    ):
        """Test successful retrieval by email."""
        mock_user_repository.get_by_email.return_value = sample_user

        result = user_service.get_user_by_email(sample_user.email)

        assert result == sample_user

    def test_get_user_by_email_not_found(self, user_service, mock_user_repository):
        """Test raises UserNotFoundException when email not found."""
        mock_user_repository.get_by_email.return_value = None

        with pytest.raises(UserNotFoundException) as exc_info:
            user_service.get_user_by_email("nonexistent@example.com")

        assert "nonexistent@example.com" in str(exc_info.value)

    def test_get_user_by_email_database_error(self, user_service, mock_user_repository):
        """Test wraps DatabaseException in UserServiceException."""
        mock_user_repository.get_by_email.side_effect = DatabaseException("Error")

        with pytest.raises(UserServiceException) as exc_info:
            user_service.get_user_by_email("test@example.com")

        assert "Failed to retrieve user data" in str(exc_info.value)


class TestGetUserByEmailOrNone:
    """Tests for get_user_by_email_or_none method."""

    def test_get_user_by_email_or_none_success(
        self, user_service, mock_user_repository, sample_user
    ):
        """Test returns user when found."""
        mock_user_repository.get_by_email.return_value = sample_user

        result = user_service.get_user_by_email_or_none(sample_user.email)

        assert result == sample_user

    def test_get_user_by_email_or_none_not_found(
        self, user_service, mock_user_repository
    ):
        """Test returns None when email not found."""
        mock_user_repository.get_by_email.return_value = None

        result = user_service.get_user_by_email_or_none("missing@example.com")

        assert result is None

    def test_get_user_by_email_or_none_database_error(
        self, user_service, mock_user_repository
    ):
        """Test returns None on database error."""
        mock_user_repository.get_by_email.side_effect = DatabaseException("Failed")

        result = user_service.get_user_by_email_or_none("test@example.com")

        assert result is None


class TestListUsers:
    """Tests for list_users method."""

    def test_list_users_success(
        self, user_service, mock_user_repository, sample_user, another_user
    ):
        """Test returns list of users."""
        mock_user_repository.list.return_value = [sample_user, another_user]

        result = user_service.list_users()

        assert len(result) == 2
        assert sample_user in result
        assert another_user in result

    def test_list_users_empty(self, user_service, mock_user_repository):
        """Test returns empty list when no users."""
        mock_user_repository.list.return_value = []

        result = user_service.list_users()

        assert result == []

    def test_list_users_database_error(self, user_service, mock_user_repository):
        """Test wraps DatabaseException in UserServiceException."""
        mock_user_repository.list.side_effect = DatabaseException("Connection lost")

        with pytest.raises(UserServiceException) as exc_info:
            user_service.list_users()

        assert "Failed to retrieve user list" in str(exc_info.value)


class TestUpdateUser:
    """Tests for update_user method."""

    def test_update_user_success(self, user_service, mock_user_repository, sample_user):
        """Test successful user update."""
        existing = Mock()
        existing.id = sample_user.id
        mock_user_repository.get_by_id.return_value = existing
        mock_user_repository.get_by_email.return_value = None
        mock_user_repository.get_by_username.return_value = None
        mock_user_repository.update.return_value = sample_user

        result = user_service.update_user(sample_user)

        assert result == sample_user
        mock_user_repository.update.assert_called_once_with(sample_user)

    def test_update_user_not_found(
        self, user_service, mock_user_repository, sample_user
    ):
        """Test raises UserNotFoundException when user doesn't exist."""
        mock_user_repository.get_by_id.return_value = None

        with pytest.raises(UserNotFoundException) as exc_info:
            user_service.update_user(sample_user)

        assert str(sample_user.id) in str(exc_info.value)

    def test_update_user_duplicate_email(
        self, user_service, mock_user_repository, sample_user, another_user
    ):
        """Test raises EmailAlreadyExistsException when changing to existing email."""
        existing = Mock()
        existing.id = sample_user.id
        existing.email = "old@example.com"
        existing.username = sample_user.username

        another_user.id = uuid4()  # Different ID

        mock_user_repository.get_by_id.return_value = existing
        mock_user_repository.get_by_email.return_value = another_user

        sample_user.email = another_user.email  # Try to change to existing email

        with pytest.raises(EmailAlreadyExistsException) as exc_info:
            user_service.update_user(sample_user)

        assert "already used by another user" in str(exc_info.value)

    def test_update_user_same_email_different_user(
        self, user_service, mock_user_repository, sample_user
    ):
        """Test allows keeping same email."""
        existing = Mock()
        existing.id = sample_user.id
        existing.email = sample_user.email
        existing.username = "oldusername"

        mock_user_repository.get_by_id.return_value = existing
        # Should not check email since it's the same
        mock_user_repository.get_by_username.return_value = None
        mock_user_repository.update.return_value = sample_user

        result = user_service.update_user(sample_user)

        assert result == sample_user

    def test_update_user_duplicate_entry_exception(
        self, user_service, mock_user_repository, sample_user
    ):
        """Test DuplicateEntryException from repository."""
        existing = Mock()
        existing.id = sample_user.id
        existing.email = sample_user.email
        existing.username = sample_user.username

        mock_user_repository.get_by_id.return_value = existing
        mock_user_repository.update.side_effect = DuplicateEntryException("Conflict")

        with pytest.raises(EmailAlreadyExistsException) as exc_info:
            user_service.update_user(sample_user)

        assert "already used by another user" in str(exc_info.value)

    def test_update_user_database_error(
        self, user_service, mock_user_repository, sample_user
    ):
        """Test wraps DatabaseException in UserServiceException."""
        existing = Mock()
        existing.id = sample_user.id
        existing.email = sample_user.email
        existing.username = sample_user.username

        mock_user_repository.get_by_id.return_value = existing
        mock_user_repository.update.side_effect = DatabaseException("Timeout")

        with pytest.raises(UserServiceException) as exc_info:
            user_service.update_user(sample_user)

        assert "Failed to update user" in str(exc_info.value)


class TestDeleteUser:
    """Tests for delete_user method."""

    def test_delete_user_success(self, user_service, mock_user_repository, sample_user):
        """Test successful user deletion."""
        mock_user_repository.get_by_id.return_value = sample_user

        user_service.delete_user(sample_user.id)

        mock_user_repository.delete.assert_called_once_with(sample_user.id)

    def test_delete_user_not_found(self, user_service, mock_user_repository):
        """Test raises UserNotFoundException when user doesn't exist."""
        mock_user_repository.get_by_id.return_value = None

        with pytest.raises(UserNotFoundException) as exc_info:
            user_service.delete_user(uuid4())

        assert "not found" in str(exc_info.value)
        mock_user_repository.delete.assert_not_called()

    def test_delete_user_database_error_on_get(
        self, user_service, mock_user_repository, sample_user
    ):
        """Test wraps DatabaseException from get_by_id."""
        mock_user_repository.get_by_id.side_effect = DatabaseException("Error")

        with pytest.raises(UserServiceException) as exc_info:
            user_service.delete_user(sample_user.id)

        assert "Failed to delete user" in str(exc_info.value)

    def test_delete_user_database_error_on_delete(
        self, user_service, mock_user_repository, sample_user
    ):
        """Test wraps DatabaseException from delete."""
        mock_user_repository.get_by_id.return_value = sample_user
        mock_user_repository.delete.side_effect = DatabaseException("Cannot delete")

        with pytest.raises(UserServiceException) as exc_info:
            user_service.delete_user(sample_user.id)

        assert "Failed to delete user" in str(exc_info.value)


class TestValidateNewUser:
    """Tests for _validate_new_user private method."""

    def test_validate_valid_user(self, user_service, mock_user_repository, sample_user):
        """Test passes with valid user data."""
        mock_user_repository.get_by_email.return_value = None
        mock_user_repository.get_by_username.return_value = None

        # Should not raise
        user_service._validate_new_user(sample_user)

    def test_validate_invalid_email_no_at(self, user_service, sample_user):
        """Test fails with email missing @."""
        sample_user.email = "invalidemail.com"

        with pytest.raises(ValidationException):
            user_service._validate_new_user(sample_user)

    def test_validate_empty_email(self, user_service, sample_user):
        """Test fails with empty email."""
        sample_user.email = ""

        with pytest.raises(ValidationException):
            user_service._validate_new_user(sample_user)

    def test_validate_empty_username(self, user_service, sample_user):
        """Test fails with empty username."""
        sample_user.username = ""

        with pytest.raises(ValidationException):
            user_service._validate_new_user(sample_user)

    def test_validate_two_char_username(self, user_service, sample_user):
        """Test fails with 2-character username."""
        sample_user.username = "ab"

        with pytest.raises(ValidationException):
            user_service._validate_new_user(sample_user)

    def test_validate_exactly_three_char_username(
        self, user_service, mock_user_repository, sample_user
    ):
        """Test passes with exactly 3-character username."""
        sample_user.username = "abc"
        mock_user_repository.get_by_email.return_value = None
        mock_user_repository.get_by_username.return_value = None

        # Should not raise
        user_service._validate_new_user(sample_user)


class TestValidateUpdateUser:
    """Tests for _validate_update_user private method."""

    def test_validate_update_same_data(
        self, user_service, mock_user_repository, sample_user
    ):
        """Test passes when no changes made."""
        existing = Mock()
        existing.email = sample_user.email
        existing.username = sample_user.username

        mock_user_repository.get_by_email.return_value = None
        mock_user_repository.get_by_username.return_value = None

        # Should not raise
        user_service._validate_update_user(sample_user, existing)

    def test_validate_update_new_email_conflict(
        self, user_service, mock_user_repository, sample_user, another_user
    ):
        """Test fails when changing to existing email."""
        existing = Mock()
        existing.email = "old@example.com"
        existing.username = sample_user.username

        another_user.id = uuid4()  # Different ID

        mock_user_repository.get_by_email.return_value = another_user

        with pytest.raises(EmailAlreadyExistsException):
            user_service._validate_update_user(sample_user, existing)

    def test_validate_update_new_username_conflict(
        self, user_service, mock_user_repository, sample_user, another_user
    ):
        """Test fails when changing to existing username."""
        existing = Mock()
        existing.email = sample_user.email
        existing.username = "oldusername"

        another_user.id = uuid4()  # Different ID

        mock_user_repository.get_by_email.return_value = None
        mock_user_repository.get_by_username.return_value = another_user

        with pytest.raises(UsernameAlreadyExistsException):
            user_service._validate_update_user(sample_user, existing)

    def test_validate_update_email_to_same_value(
        self, user_service, mock_user_repository, sample_user
    ):
        """Test passes when email unchanged."""
        existing = Mock()
        existing.email = sample_user.email
        existing.username = "oldusername"

        # Should not query email since unchanged
        mock_user_repository.get_by_username.return_value = None

        # Should not raise
        user_service._validate_update_user(sample_user, existing)
        mock_user_repository.get_by_email.assert_not_called()


class TestIntegrationScenarios:
    """Integration-style tests for complex scenarios."""

    def test_create_then_get_user(
        self, user_service, mock_user_repository, sample_user
    ):
        """Test full flow of creating and retrieving user."""
        # Setup for create
        mock_user_repository.get_by_email.return_value = None
        mock_user_repository.get_by_username.return_value = None
        mock_user_repository.create.return_value = sample_user

        # Create
        created = user_service.create_user(sample_user)
        assert created == sample_user

        # Setup for get
        mock_user_repository.get_by_id.return_value = sample_user

        # Get
        retrieved = user_service.get_user(created.id)
        assert retrieved == created

    def test_update_deleted_user(self, user_service, mock_user_repository, sample_user):
        """Test updating user that was deleted between check and update."""
        existing = Mock()
        existing.id = sample_user.id
        existing.email = sample_user.email
        existing.username = sample_user.username

        mock_user_repository.get_by_id.return_value = existing
        mock_user_repository.update.side_effect = NotFoundException("User gone")

        with pytest.raises(UserNotFoundException):
            user_service.update_user(sample_user)

    def test_concurrent_update_simulation(
        self, user_service, mock_user_repository, sample_user
    ):
        """Simulate concurrent update conflict."""
        existing = Mock()
        existing.id = sample_user.id
        existing.email = "old@example.com"
        existing.username = "oldname"

        # First check passes, but update fails due to race condition
        mock_user_repository.get_by_id.return_value = existing
        mock_user_repository.update.side_effect = DuplicateEntryException(
            "Duplicate key"
        )

        with pytest.raises(EmailAlreadyExistsException):
            user_service.update_user(sample_user)
