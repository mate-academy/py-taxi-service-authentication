from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("taxi.urls", namespace="taxi")),
    path(
        "accounts/login/",
        LoginView.as_view(
            template_name="registration/login.html"
        ),
        name="login",
    ),
    path(
        "accounts/logout/",
        LogoutView.as_view(),
        name="logout",
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
