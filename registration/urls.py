from django.urls import path
from .views import TaxiLoginView, TaxiLogoutView


urlpatterns = [
    path(
        "login/",
        TaxiLoginView.as_view(template_name="registration/login.html"),
        name="login"
    ),
    path("logout/", TaxiLogoutView.as_view(), name="logout"),
]
