from django.urls import path

from taxi.views import (
    CarDetailView,
    CarsListView,
    DriverDetailView,
    DriversListView,
    HomePageView,
    ManufacturerDetailView,
    ManufacturersListView,
)

app_name = "taxi"
urlpatterns = [
    path("", HomePageView.as_view(), name="index"),
    path(
        "manufacturers/",
        ManufacturersListView.as_view(),
        name="manufacturer-list"
    ),
    path(
        "manufacturer/<int:pk>/",
        ManufacturerDetailView.as_view(),
        name="manufacturer-detail"
    ),
    path("cars/", CarsListView.as_view(), name="car-list"),
    path("car/<int:pk>/", CarDetailView.as_view(), name="car-detail"),
    path("drivers/", DriversListView.as_view(), name="driver-list"),
    path(
        "driver/<int:pk>/",
        DriverDetailView.as_view(),
        name="driver-detail"
    ),
]
