from django.contrib.auth import views as auth_views
from django.urls import path

from taxi.views import (
    CarDetailView,
    CarListView,
    DriverDetailView,
    DriverListView,
    ManufacturerListView,
    index,
)

app_name = "taxi"

urlpatterns = [
    path("", index, name="index"),
    path("accounts/login/", auth_views.LoginView.as_view(), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("manufacturers/", ManufacturerListView.as_view(), name="manufacturer-list"),
    path("cars/", CarListView.as_view(), name="car-list"),
    path("cars/<int:pk>/", CarDetailView.as_view(), name="car-detail"),
    path("drivers/", DriverListView.as_view(), name="driver-list"),
    path("drivers/<int:pk>/", DriverDetailView.as_view(), name="driver-detail"),
]
