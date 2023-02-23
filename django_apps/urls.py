from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/v1/', include('django_apps.users.urls'))
]
