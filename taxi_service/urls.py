from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from taxi.views import CustomLoginView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("taxi.urls", namespace="taxi")),
    path("accounts/login/", CustomLoginView.as_view(), name="login"),
    path("accounts/", include("django.contrib.auth.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
