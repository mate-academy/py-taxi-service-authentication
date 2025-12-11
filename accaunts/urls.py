from django.urls import path, include

from accaunts.views import login_view, logout_view


app_name = "accounts"

urlpatterns = [
    path("login/", login_view),
    path("logouth/", logout_view),
]
