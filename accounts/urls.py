from django.urls import path, include
from accounts.views import login, logout_view

urlpatterns = [
    path("", login, namespace=login),
]
