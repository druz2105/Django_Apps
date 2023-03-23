from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (UserSerializer, CustomTokenObtainPairSerializer, UserUpdateSerializer, UserDetailSerializer,
                          ProfileImageSerializer, ChangePasswordSerializer)
from .services import UserServices


# Create your views here.


class UserRegisterView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CustomObtainJWTView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class CustomRefreshJWTView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserDetailUpdateView(RetrieveUpdateDestroyAPIView):
    service = UserServices()

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method in ['PUT', "PATCH"]:
            return UserUpdateSerializer
        else:
            return UserDetailSerializer

    def update(self, request, *args, **kwargs):
        kwargs.update({'partial': True})
        return super().update(request, args, kwargs)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.delete()


class ProfileImageCreateView(CreateAPIView):
    serializer_class = ProfileImageSerializer

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.pk
        return super().create(request, *args, **kwargs)


class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.get_object().check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.get_object().set_password(serializer.data.get("new_password"))
            self.get_object().save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
