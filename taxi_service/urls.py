"""taxi_service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path("", views.home, name="home")
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path("", Home.as_view(), name="home")
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path("blog/", include("blog.urls"))
"""

from django.contrib import admin
from django.urls import path, include
from taxi.views import (
    index,
    DriverListView,
    CarListView,
    ManufacturerListView,
    DriverDetailView,
    CarDetailView
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name="index"),
    path("drivers/", DriverListView.as_view(), name="driver-list"),
    path("cars/", CarListView.as_view(), name="car-list"),
    path("manufacturers/", ManufacturerListView.as_view(),
         name="manufacturer-list"),
    path("drivers/<int:pk>/", DriverDetailView.as_view(),
         name="driver-detail"),
    path("cars/<int:pk>/", CarDetailView.as_view(), name="car-detail"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include(("taxi.urls", "taxi"), namespace="taxi")),
]
