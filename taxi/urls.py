from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import index, CarListView, CarDetailView, DriverListView, DriverDetailView, ManufacturerListView

urlpatterns = [
    path("", index, name="index"),
    path("manufacturers/", ManufacturerListView.as_view(), name="manufacturer_list"),
    path("cars/", CarListView.as_view(), name="car_list"),
    path("cars/<int:pk>/", CarDetailView.as_view(), name="car_detail"),
    path("drivers/", DriverListView.as_view(), name="driver_list"),
    path("drivers/<int:pk>/", DriverDetailView.as_view(), name="driver_detail"),
    #path("/login/", LoginView.as_view()),
    #path("/logout/", LogoutView.as_view())
]

app_name = "taxi"
