from django.urls import path

from .views import (
    index,
    CarListView,
    CarDetailView,
    DriverListView,
    DriverDetailView,
    ManufacturerListView, CarCreate, CarUpdate, CarDelete, ManufacturerCreate, ManufacturerUpdate, ManufacturerDelete,
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
    path("cars/create", CarCreate.as_view(), name="driver-create"),
    path("cars/update", CarUpdate.as_view(), name="driver-update"),
    path("cars/delete", CarDelete.as_view(), name="driver-delete"),
    path("manufacturer/create", ManufacturerCreate.as_view(), name="manufacturer-create"),
    path("manufacturer/update", ManufacturerUpdate.as_view(), name="manufacturer-update"),
    path("manufacturer/delete", ManufacturerDelete.as_view(), name="manufacturer-delete"),
]

app_name = "taxi"
