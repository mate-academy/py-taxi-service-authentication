from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from taxi.views import PostRedirectGetLoginView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/login/", PostRedirectGetLoginView.as_view(), name="login"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include(("taxi.urls", "taxi"), namespace="taxi")),
]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )
