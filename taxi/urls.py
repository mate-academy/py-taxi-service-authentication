from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

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
    path("taxi/", index, name="index"),
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
]

app_name = "taxi"
