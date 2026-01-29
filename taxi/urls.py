# Em taxi_service/urls.py (ou o nome do seu diretório de configurações)

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),

    # URLs de Autenticação (Usando nomes de URL com hífens)
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="taxi/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="login"),
        name="logout"
    ),

    # Incluir URLs do app
    path("", include("taxi.urls")),
]
