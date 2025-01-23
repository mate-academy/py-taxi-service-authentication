from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include

from .views import (
    index,
    CarListView,
    CarDetailView,
    DriverListView,
    DriverDetailView,
    ManufacturerListView,
    RegisterForm
)

urlpatterns = [
    path("", index, name="index"),
    path(
        "manufacturers/",
        ManufacturerListView.as_view(),
        name="manufacturer-list",
    ),
    path("cars/", CarListView.as_view(), name="car-list"),
    path("cars/<int:pk>/", CarDetailView.as_view(), name="car-detail"),
    path("drivers/", DriverListView.as_view(), name="driver-list"),
    path(
        "drivers/<int:pk>/", DriverDetailView.as_view(), name="driver-detail"
    ),
    path("accounts/", include('django.contrib.auth.urls')),
    path("login/", LoginView.as_view, name="login"),
    path("logout/", LogoutView.as_view, name="logout"),
]

app_name = "taxi"
