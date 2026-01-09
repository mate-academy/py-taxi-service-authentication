from django.conf.global_settings import LOGIN_URL
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import Driver, Car, Manufacturer


@login_required(login_url="/accounts/login/")
def index(request):
    """View function for the home page of the site."""

    num_drivers = Driver.objects.count()
    num_cars = Car.objects.count()
    num_manufacturers = Manufacturer.objects.count()
    num_visits = request.session.get("num_visits", 0) + 1
    request.session["num_visits"] = num_visits  # Set the visit count directly

    context = {
        "num_drivers": num_drivers,
        "num_cars": num_cars,
        "num_manufacturers": num_manufacturers,
        "num_visits": num_visits,
    }

    return render(request, "taxi/index.html", context=context)


class CustomLoginView(LoginView):
    template_name = "registration/login.html"


class ManufacturerListView(LoginRequiredMixin, ListView):
    model = Manufacturer
    context_object_name = "manufacturer_list"
    template_name = "taxi/manufacturer_list.html"
    paginate_by = 5


class CarListView(LoginRequiredMixin, ListView):
    model = Car
    paginate_by = 5
    queryset = Car.objects.select_related("manufacturer").order_by("id")
    login_url = "/accounts/login/"
    template_name = "taxi/car_list.html"


class CarDetailView(generic.DetailView):
    model = Car


class DriverListView(LoginRequiredMixin, generic.ListView):
    model = Driver
    paginate_by = 5
    login_url = LOGIN_URL


class DriverDetailView(generic.DetailView):
    model = Driver
    queryset = Driver.objects.prefetch_related("cars__manufacturer")
