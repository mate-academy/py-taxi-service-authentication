from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (
    # home,
    CarListView,
    CarDetailView,
    DriverListView,
    DriverDetailView,
    ManufacturerListView,
    IndexView,

)

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path(
        "manufacturers/",
        ManufacturerListView.as_view(),
        name="manufacturer-list",
    ),
    path("cars/", CarListView.as_view(), name="car-list"),
    path("cars/<int:pk>/", CarDetailView.as_view(), name="car-detail"),
    path("drivers/", DriverListView.as_view(), name="driver-list"),
    path(
        "drivers/<int:pk>/",
        DriverDetailView.as_view(),
        name="driver-detail"
    ),
    path(
        "manufacturers/",
        ManufacturerListView.as_view(),
        name="manufacturer-list"
    ),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="registration/login.html"
        ), name="login"
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(
            template_name="registration/logged-out.html"
        ), name="logout"
    ),
]

app_name = "taxi"
