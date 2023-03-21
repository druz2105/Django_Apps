from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .services import UserServices
from .serializers import UserSerializer, CustomTokenObtainPairSerializer, UserUpdateSerializer, UserDetailSerializer, \
    ProfileImageSerializer


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
