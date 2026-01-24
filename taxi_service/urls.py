from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("taxi.urls", namespace="taxi")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("logout/", LogoutView.as_view()),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
