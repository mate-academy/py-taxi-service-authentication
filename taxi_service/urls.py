# Em taxi_service/urls.py (ou o nome do seu diretório de configurações)

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views  # Correção: Dois espaços antes do comentário

urlpatterns = [
    path("admin/", admin.site.urls),  # Correção: Aspas duplas (Q000)

    # URLs de Autenticação (Usando nomes de URL com hífens)
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="taxi/login.html"),
        name="login",
    ),  # Correção: Linhas longas quebradas e aspas duplas
    path(
        "logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"
    ),  # Correção: Linhas longas quebradas, aspas duplas e remoção de espaços

    # Incluir URLs do app
    path("", include("taxi.urls")),  # Correção: Aspas duplas (Q000)
]
