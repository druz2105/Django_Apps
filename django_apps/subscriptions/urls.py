from django.urls import path

from . import views

urlpatterns = [
    path('plans/', views.SubscriptionPlansListView.as_view(), name='plans'),
    path('create/', views.CreateSubscriptionView.as_view(), name='subscribe'),
    path('validate/', views.ValidateSubscriptionAPIView.as_view(), name='check_subscription'),
    path('verify/', views.VerifySubscriptionAPIView.as_view(), name='check_subscription'),
]
