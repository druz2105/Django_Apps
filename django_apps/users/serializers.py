from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, UserProfileImages


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']

    def create(self, validated_data) -> User:
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.is_active = True
        user.set_password(password)
        user.save()
        return user


# noinspection PyUnresolvedReferences
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user) -> dict:
        token = super().get_token(user)

        # Add custom claims
        token['id'] = user.id

        return token

    def validate(self, attrs) -> dict:
        data = super().validate(attrs)
        data['id'] = self.user.id
        data['first_name'] = self.user.first_name
        data['last_name'] = self.user.last_name
        data['email'] = self.user.email
        return data


class CustomTokenRefreshPairSerializer(TokenRefreshSerializer):

    @staticmethod
    def get_user_from_refresh_token(refresh_token):
        """
        Takes in a refresh token and returns the user it belongs to
        """
        try:
            token = RefreshToken(refresh_token)
            user_id = token.payload['user_id']
            user = get_user_model().objects.get(id=user_id)
            return user
        except Exception as e:
            # Handle any errors that may occur
            print(str(e))
            return None

    def validate(self, attrs) -> dict:
        data = super().validate(attrs)
        user = self.get_user_from_refresh_token(data["refresh"])
        data['user_id'] = user.id
        data['first_name'] = user.first_name
        data['last_name'] = user.last_name
        data['email'] = user.email
        return data


class UserUpdateSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'last_login']


class UserDetailSerializer(UserUpdateSerializer):
    email = serializers.CharField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    image = serializers.SerializerMethodField()

    class Meta(UserUpdateSerializer.Meta):
        fields = UserUpdateSerializer.Meta.fields + ['image']

    def get_image(self, user):
        if user.profile_images.first():
            return user.profile_images.first().images.url
        return ''


class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfileImages
        fields = ['user', 'images']

    def create(self, validated_data):
        user = self.context.get('request').user
        with transaction.atomic():
            user.profile_images.all().delete()
            return super().create(validated_data)
