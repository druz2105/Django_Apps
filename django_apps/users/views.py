from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .services import UserServices
from .serializers import UserSerializer, CustomTokenObtainPairSerializer, UserUpdateSerializer, UserDetailSerializer, \
    ProfileImageSerializer


# Create your views here.


class UserRegisterView(CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CustomObtainJWTView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class CustomRefreshJWTView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserDetailUpdateView(RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    service = UserServices()

    def get_queryset(self):
        return self.service.get_users_queryset({'is_active': True})

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
