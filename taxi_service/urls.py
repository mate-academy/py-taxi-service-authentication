from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),

    # Auth explícito com nomes esperados nos testes
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    # Suas rotas da app
    path("", include(("taxi.urls", "taxi"), namespace="taxi")),
]
