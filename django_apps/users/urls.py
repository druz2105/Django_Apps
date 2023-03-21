from django.contrib.auth.decorators import login_required
from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView

from . import views

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/', views.CustomObtainJWTView.as_view(), name='login'),
    path('verify/', TokenVerifyView.as_view(), name='verify'),
    path('refresh/', views.CustomRefreshJWTView.as_view(), name='refresh'),
    path('user/details/', views.UserDetailUpdateView.as_view(), name='user_detail'),
    path('user/profile/image/', views.ProfileImageCreateView.as_view(), name='user_detail'),
]
