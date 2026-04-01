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

# Ensure namespace is correctly set for the 'taxi' app
app_name = "taxi"

urlpatterns = [
    # Home Page
    path("", index, name="index"),

    # Manufacturer URLs
    path("manufacturers/", ManufacturerListView.as_view(),
         name="manufacturer-list"),

    # Car URLs
    path("cars/", CarListView.as_view(), name="car-list"),
    path("cars/<int:pk>/", CarDetailView.as_view(), name="car-detail"),

    # Driver URLs
    path("drivers/", DriverListView.as_view(), name="driver-list"),
    path("drivers/<int:pk>/", DriverDetailView.as_view(),
         name="driver-detail"),

    # Authentication URLs inside "taxi" namespace
    path("login/", auth_views.LoginView.as_view(
        template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(
        next_page="taxi:login"), name="logout"),
]
