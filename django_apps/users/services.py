from .models import User


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
