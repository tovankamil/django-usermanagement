# users/migrations/0001_initial.py

import uuid
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        # USERS
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        primary_key=True, default=uuid.uuid4, editable=False
                    ),
                ),
                ("username", models.CharField(max_length=100, unique=True)),
                ("email", models.EmailField(max_length=255, unique=True)),
                ("password_hash", models.TextField()),
                ("is_active", models.BooleanField(default=True)),
                ("is_verified", models.BooleanField(default=False)),
                ("last_login", models.DateTimeField(null=True, blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        # ROLES
        migrations.CreateModel(
            name="Role",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100, unique=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        # PERMISSIONS
        migrations.CreateModel(
            name="Permission",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("code", models.CharField(max_length=100, unique=True)),
                ("name", models.CharField(max_length=150)),
                ("description", models.TextField(blank=True, null=True)),
            ],
        ),
        # USER ROLES
        migrations.CreateModel(
            name="UserRole",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("assigned_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="users.user",
                    ),
                ),
                (
                    "role",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="users.role",
                    ),
                ),
            ],
        ),
        # ROLE PERMISSIONS
        migrations.CreateModel(
            name="RolePermission",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "role",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="users.role",
                    ),
                ),
                (
                    "permission",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="users.permission",
                    ),
                ),
            ],
        ),
        # SESSIONS
        migrations.CreateModel(
            name="Session",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("session_token", models.TextField()),
                ("ip_address", models.GenericIPAddressField()),
                ("user_agent", models.TextField()),
                ("expires_at", models.DateTimeField()),
                ("is_revoked", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="users.user",
                    ),
                ),
            ],
        ),
        # ACTIVITY LOG
        migrations.CreateModel(
            name="ActivityLog",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("action", models.CharField(max_length=100)),
                ("resource", models.CharField(max_length=100)),
                ("ip_address", models.GenericIPAddressField()),
                ("metadata", models.JSONField(null=True, blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="users.user",
                    ),
                ),
            ],
        ),
    ]
