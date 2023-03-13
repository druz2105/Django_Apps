from .models import User, UserProfileImages


class UserServices:
    model = User

    def get_user_object_id(self, id):
        return self.model.objects.get(id=id)

    def get_active_user_object_id(self, id):
        return self.model.objects.get(id=id)

    def get_all_users_queryset(self):
        return self.model.objects.all()

    def get_users_queryset(self, data: dict):
        return self.model.objects.filter(**data)


class ProfileImagesServices:
    model = UserProfileImages

    def get_images_queryset(self, data: dict):
        return self.model.objects.filter(**data)

    def get_all_images_queryset(self):
        return self.model.objects.all()
