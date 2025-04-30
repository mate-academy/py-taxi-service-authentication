from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

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
        name="manufacturer-list",
    ),
    path("cars/", CarListView.as_view(), name="car-list"),
    path("cars/<int:pk>/", CarDetailView.as_view(), name="car-detail"),
    path("drivers/", DriverListView.as_view(), name="driver-list"),
    path(
        "drivers/<int:pk>/", DriverDetailView.as_view(), name="driver-detail"
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path(
        "logged_out/",
        TemplateView.as_view(template_name="registration/logged_out.html"),
        name="logged_out",
    ),
]

app_name = "taxi"
