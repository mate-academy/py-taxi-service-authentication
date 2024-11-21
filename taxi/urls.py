from django.urls import path
from .views import (
    index,
    CarListView,
    CarDetailView,
    DriverListView,
    DriverDetailView,
    ManufacturerListView,
    login_view,
    logout_view,
)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", index, name="index"),
    path("manufacturers/", ManufacturerListView.as_view(),
         name="manufacturer-list"),
    path("cars/", CarListView.as_view(), name="car-list"),
    path("cars/<int:pk>/", CarDetailView.as_view(), name="car-detail"),
    path("drivers/", DriverListView.as_view(),
         name="driver-list"),
    path("drivers/<int:pk>/", DriverDetailView.as_view(),
         name="driver-detail"),
    path("logout/", logout_view, name="logout"),
    path("taxi/login/", auth_views.LoginView.as_view(), name="login"),
]

app_name = "taxi"
