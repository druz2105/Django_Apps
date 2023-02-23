from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from .serializers import UserSerializer


# Create your views here.


class UserRegisterView(CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        print(request.data)
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        print(serializer.is_valid())
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
