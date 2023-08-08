from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            # "phone",
            # "first_name",
            # "last_name",
            # "middle_name",
            # "date_joined",
            # "last_login",
            # "role",
        ]
        # read_only_fields = ["id", "role", "date_joined", "last_login"]


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "password",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    password = serializers.CharField(required=True, allow_blank=False, allow_null=False)


class LogoutSerializer(serializers.Serializer):
    access_token = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    refresh_token = serializers.CharField(required=True, allow_blank=False, allow_null=False)
