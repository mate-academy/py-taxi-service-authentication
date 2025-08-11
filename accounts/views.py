from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView


class TaxiLoginView(LoginView):
    template_name = "accounts/login.html"


class TaxiLogoutView(LogoutView):
    template_name = "accounts/logout.html"
