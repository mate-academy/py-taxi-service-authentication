from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from taxi.views import CustomLoginView, CustomLogoutView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("", include("taxi.urls", namespace="taxi")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
