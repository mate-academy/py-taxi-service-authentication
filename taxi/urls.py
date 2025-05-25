from tkinter.font import names

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

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
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logut/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]

app_name = "taxi"
