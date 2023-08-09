from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
        ]


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "password",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    password = serializers.CharField(required=True, allow_blank=False, allow_null=False)
