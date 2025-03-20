from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (
    index,
    CarListView,
    CarDetailView,
    DriverListView,
    DriverDetailView,
    ManufacturerListView,
)

urlpatterns = [
    path("", index, name="index"),
    path(
        "manufacturers/",
        ManufacturerListView.as_view(),
        name="manufacturer_list",
    ),
    path("cars/", CarListView.as_view(), name="car_list"),
    path("cars/<int:pk>/", CarDetailView.as_view(), name="car_detail"),
    path("drivers/", DriverListView.as_view(), name="driver_list"),
    path(
        "drivers/<int:pk>/", DriverDetailView.as_view(), name="driver_detail"
    ),
    path("login/",
         auth_views.LoginView.as_view(template_name="registration/login.html"),
         name="login"),
    path("logout/", auth_views.LogoutView.as_view(
        template_name="registration/logged_out.html"), name="logout"),
]

app_name = "taxi"
