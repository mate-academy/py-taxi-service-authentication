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

app_name = "taxi"

urlpatterns = [
    path("", index, name="index"),

    # Manufacturers
    path("manufacturers/", ManufacturerListView.as_view(),
         name="manufacturer-list"
         ),

    # Cars
    path("cars/", CarListView.as_view(), name="car-list"),
    path("cars/<int:pk>/", CarDetailView.as_view(), name="car-detail"),

    # Drivers
    path("drivers/", DriverListView.as_view(), name="driver-list"),
    path("drivers/<int:pk>/", DriverDetailView.as_view(),
         name="driver-detail"
         ),

    # Authentication
    path(
        "log-in/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="log-in",
    ),
    path(
        "log-out/",
        auth_views.LogoutView.as_view(next_page="taxi:log-in"),
        name="log-out",
    ),
]
