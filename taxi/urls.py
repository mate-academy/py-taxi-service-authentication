from django.urls import path, include

from taxi_service import settings
from .views import (
    index,
    CarListView,
    CarDetailView,
    DriverListView,
    DriverDetailView,
    ManufacturerListView
)

from django.contrib.auth import views

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
    path('login/', views.LoginView.as_view(template_name='registration/login.html'),
         name='login'),
    path('logout/', views.LogoutView.as_view(next_page='login'),
         name='logout'),
]

app_name = "taxi"
