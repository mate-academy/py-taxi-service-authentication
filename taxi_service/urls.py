from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("taxi.urls")),
    # Add this line for authentication URLs (login, logout, password management)
    path("accounts/", include("django.contrib.auth.urls")),
]
