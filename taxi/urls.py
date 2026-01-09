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

app_name = 'taxi'

urlpatterns = [
    path("", index, name="index"),
    path(
        "manufacturers/",
        ManufacturerListView.as_view(),
        name="manufacturer-list",
    ),
    path("cars/", CarListView.as_view(), name="car-list"),
    path("cars/<int:pk>/", CarDetailView.as_view(), name="car-detail"),
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path("drivers/<int:pk>/", DriverDetailView.as_view(), name="driver-detail"),
    path('drivers/', DriverListView.as_view(), name='driver-list'),
    path('home/', views.home, name='home'),
]
