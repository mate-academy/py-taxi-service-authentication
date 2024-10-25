from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    index,
    CarListView,
    CarDetailView,
    DriverListView,
    DriverDetailView,
    ManufacturerListView,
    LoginView,
)

urlpatterns = [
    path("", index, name="index"),
    path("login/",
         auth_views.LoginView.as_view(
             template_name="templates/registration/login.html"),
         name="login"),
    path("logout/",
         auth_views.LogoutView.as_view(template_name="taxi/logout.html"),
         name="logout"),
    path("login/", LoginView.as_view(), name="login"),
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

]

app_name = "taxi"
