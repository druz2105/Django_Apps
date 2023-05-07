from typing import Union

from django.core.exceptions import ObjectDoesNotExist
from django.http import QueryDict

from .models import User, UserProfileImages, UserSubscription


class UserServices:
    model = User

    def get_user_object_id(self, id) -> User:
        return self.model.objects.get(id=id)

    def get_active_user_object_id(self, id) -> User:
        return self.model.objects.get(id=id)

    def get_all_users_queryset(self) -> QueryDict[User]:
        return self.model.objects.all()

    def get_users_queryset(self, data: dict) -> QueryDict[User]:
        return self.model.objects.filter(**data)

    @staticmethod
    def get_user_subscription(user) -> Union[UserSubscription, None]:
        try:
            return user.subscriptions
        except ObjectDoesNotExist:
            return None


class ProfileImagesServices:
    model = UserProfileImages

    def get_images_queryset(self, data: dict) -> QueryDict[UserProfileImages]:
        return self.model.objects.filter(**data)

    def get_all_images_queryset(self) -> QueryDict[UserProfileImages]:
        return self.model.objects.all()


class UserSubscriptionService:
    model = UserSubscription

    def create(self, data: dict) -> UserSubscription:
        return self.model.objects.create(**data)

    def create_or_update(self, data: dict) -> UserSubscription:
        user_subscription = self.model.objects.filter(user=data['user'])
        if user_subscription.exists():
            user_subscription.subscription_id = data['subscription_id']
            user_subscription.price_id = data['price_id']
            user_subscription.prod_id = data['prod_id']
            user_subscription.status = data['status']
            user_subscription.save()
        else:
            return self.create(data)

    def get_obj(self, data: dict) -> UserSubscription:
        return self.model.objects.get(**data)
