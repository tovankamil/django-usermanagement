import uuid
from django.db import models
from .user import User
from .role import Role


class UserRole(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    assigned_at = models.DateTimeField(auto_now_add=True)
