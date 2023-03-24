from django.urls import path

from . import views

urlpatterns = [
    path('plans/', views.SubscriptionPlansListView.as_view(), name='plans'),
    path('create/', views.CreateSubscriptionView.as_view(), name='subscribe'),
]
