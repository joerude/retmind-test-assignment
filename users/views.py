from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework import exceptions, generics, response, status
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    LoginSerializer,
    RegistrationSerializer,
    UserSerializer,
)


class UserLoginView(generics.GenericAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        user = authenticate(**serializer.validated_data)
        if not user:
            raise exceptions.AuthenticationFailed()
        user.last_login = timezone.now()
        user.save()

        refresh = RefreshToken.for_user(user)
        data = {
            "user": UserSerializer(instance=user, context={"request": request}).data,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        return response.Response(data=data, status=status.HTTP_200_OK)


class UserRegistrationView(generics.GenericAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        data = {
            "user": UserSerializer(instance=user, context={"request": request}).data,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        return response.Response(data=data, status=status.HTTP_201_CREATED)
