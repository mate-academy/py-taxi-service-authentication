from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("django.contrib.auth.urls")),
    path("", include("taxi.urls", namespace="taxi")),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
