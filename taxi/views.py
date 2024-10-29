from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.http.request import HttpRequest
from django.http.response import HttpResponse

from taxi.models import Driver, Car, Manufacturer


@login_required
def index(request: HttpRequest) -> HttpResponse:
    """View function for the home page of the site."""
    if not request.session.get("num_visits"):
        request.session["num_visits"] = 0

    num_drivers = Driver.objects.count()
    num_cars = Car.objects.count()
    num_manufacturers = Manufacturer.objects.count()
    request.session["num_visits"] = request.session.get("num_visits") + 1
    context = {
        "num_drivers": num_drivers,
        "num_cars": num_cars,
        "num_manufacturers": num_manufacturers,
        "num_visits": request.session.get("num_visits"),
    }

    print(request.user)
    return render(request, "taxi/index.html", context=context)


class ManufacturerListView(LoginRequiredMixin, ListView):
    model = Manufacturer
    queryset = Manufacturer.objects.all().order_by("name")
    paginate_by = 5
    context_object_name = "manufacturer_list"


class CarListView(LoginRequiredMixin, ListView):
    model = Car
    queryset = Car.objects.all().select_related("manufacturer")
    paginate_by = 5
    context_object_name = "car_list"


class CarDetailView(LoginRequiredMixin, DetailView):
    model = Car
    context_object_name = "car"


class DriverListView(LoginRequiredMixin, ListView):
    model = Driver
    paginate_by = 5
    context_object_name = "driver_list"


class DriverDetailView(LoginRequiredMixin, DetailView):
    model = Driver
    queryset = Driver.objects.prefetch_related("cars")
    context_object_name = "driver"
