from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView


app_name = "accounts"

urlpatterns = [
    path(
        "login/",

        LoginView.as_view(template_name="account/login.html"),
        name="login"
    ),
    path(
        "logout/",
        LogoutView.as_view(template_name="account/logged_out.html"),
        name="logout"
    )

]
