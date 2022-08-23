from django.contrib.auth.decorators import login_required
from django.urls import path

from taxi.views import (
    index,
    CarListView,
    CarDetailView,
    DriverListView,
    DriverDetailView,
    ManufacturerListView
)

urlpatterns = [
    path(
        "",
        login_required(index),
        name="index"
    ),
    path(
        "manufacturers/",
        login_required(ManufacturerListView.as_view()),
        name="manufacturer_list"
    ),
    path(
        "cars/",
        login_required(CarListView.as_view()),
        name="car_list"
    ),
    path(
        "cars/<int:pk>/",
        login_required(CarDetailView.as_view()),
        name="car_detail"
    ),
    path(
        "drivers/",
        login_required(DriverListView.as_view()),
        name="driver_list"
    ),
    path(
        "drivers/<int:pk>/",
        login_required(DriverDetailView.as_view()),
        name="driver_detail"
    ),
]

app_name = "taxi"
