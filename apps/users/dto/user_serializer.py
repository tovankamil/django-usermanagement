from rest_framework import serializers
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as ValError


class UserCreateSerializer(serializers.Serializer):

    username = serializers.CharField(
        max_length=100,
        min_length=3,
        required=True,
        trim_whitespace=True,
        error_messages={
            "required": "Username must be filled",
            "min_length": "Username min 3 character",
            "max_length": "Username max  100 character",
            "blank ": "username cannot be empty",
        },
    )

    email = serializers.EmailField(
        required=True,
        error_messages={
            "required": "Email cannot be empty",
            "invalid": "Invalid email format",
        },
    )

    password = serializers.CharField(
        write_only=True,  # Tidak akan ditampilkan di response
        required=True,
        min_length=8,
        error_messages={
            "required": "Password cannit be empty.",
            "min_length": "Password min 8 character.",
        },
    )

    first_name = serializers.CharField(
        max_length=150, required=False, allow_blank=True, default=""
    )

    last_name = serializers.CharField(
        max_length=150, required=False, allow_blank=True, default=""
    )

    phone_number = serializers.CharField(
        max_length=20, required=False, allow_blank=True, default=""
    )

    def validate_username(self, value:str)->:
        
        if not value.isalnum() and not all(c in '_' in value if not c.isalnum()):
            raise serializers.ValidationError(
                'Username only contain character, number and dash'
            )
        reserved_username = ['admin','root','system']
        if value.lower() in reserved_username:
            raise serializers.ValidationError(
                f"username {value} forbidder"
            )
            
        email = value.lower().strip()
        
        return email