from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView

from . import views

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/', views.CustomObtainJWTView.as_view(), name='login'),
    path('verify/', TokenVerifyView.as_view(), name='verify'),
    path('refresh/', views.CustomRefreshJWTView.as_view(), name='refresh'),
    path('details/', views.UserDetailUpdateView.as_view(), name='user_detail'),
    path('profile/image/', views.ProfileImageCreateView.as_view(), name='user_image'),
    path('change/password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('stripe/details/', views.UserStripeDetailsAPI.as_view(), name='stripe_details'),
    path('card/update/', views.UserCardUpdateAPI.as_view(), name='card_update')
]
