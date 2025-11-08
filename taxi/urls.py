from django.urls import path
from .views import (
    DriverListView,
    DriverDetailView,
)

app_name = "taxi"

urlpatterns = [
    path(
        "drivers/",
        DriverListView.as_view(),
        name="driver-list"
    ),
    path(
        "drivers/<int:pk>/",
        DriverDetailView.as_view(),
        name="driver-detail"
    ),
]
