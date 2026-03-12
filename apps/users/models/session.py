import uuid

from django.db import models
from .user import User


class Session(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_token = models.TextField()

    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()

    expires_at = models.DateTimeField()

    is_revoked = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
