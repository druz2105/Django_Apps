from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']
