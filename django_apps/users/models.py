from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    customer_id = models.CharField(max_length=30, null=True, blank=True, editable=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class UserProfileImages(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profile_images")
    images = models.ImageField(upload_to='profileImage/')

    def __str__(self):
        return self.user.email


class UserSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="subscriptions")
    subscription_id = models.CharField(max_length=50, null=True, blank=True)
    price_id = models.CharField(max_length=50, null=True, blank=True)
    prod_id = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} | {self.subscription_id}"

    class Meta:
        ordering = ('-created_at',)
