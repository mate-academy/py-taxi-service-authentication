from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic

from taxi.models import Car, Driver, Manufacturer


@login_required
def index(request: HttpRequest) -> HttpResponse:
    num_drivers = Driver.objects.count()
    num_manufacturers = Manufacturer.objects.count()
    num_cars = Car.objects.count()

    num_visits = request.session.get("num_visits", 0) + 1
    request.session["num_visits"] = num_visits

    context = {
        "num_drivers": num_drivers,
        "num_manufacturers": num_manufacturers,
        "num_cars": num_cars,
        "num_visits": num_visits,
    }

    return render(request, "taxi/index.html", context=context)


class ManufacturerListView(LoginRequiredMixin, generic.ListView):
    model = Manufacturer
    context_object_name = "manufacturer_list"
    template_name = "taxi/manufacturer_list.html"
    paginate_by = 5
    queryset = Manufacturer.objects.all().order_by("name")


class CarListView(LoginRequiredMixin, generic.ListView):
    model = Car
    queryset = Car.objects.all().order_by("id")
    paginate_by = 5
    queryset = Car.objects.all().select_related("manufacturer")


class CarDetailView(LoginRequiredMixin, generic.DetailView):
    model = Car
    queryset = Car.objects.all().order_by("id")


class DriverListView(LoginRequiredMixin, generic.ListView):
    model = Driver
    queryset = Driver.objects.all().order_by("id")
    paginate_by = 5


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = Driver
    queryset = Driver.objects.all().order_by("id")
    queryset = Driver.objects.all().prefetch_related("cars__manufacturer")
