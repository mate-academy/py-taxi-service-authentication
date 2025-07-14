from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import generic
from taxi.models import Manufacturer, Car, Driver


@login_required
def index(request):
    num_drivers = Driver.objects.count()
    num_cars = Car.objects.count()
    num_manufacturers = Manufacturer.objects.count()
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_drivers": num_drivers,
        "num_cars": num_cars,
        "num_manufacturers": num_manufacturers,
        "num_visits": num_visits + 1,
    }
    return render(request, "taxi/index.html", context)


class ManufacturerListView(LoginRequiredMixin, generic.ListView):
    model = Manufacturer
    paginate_by = 5
    ordering = ["name"]


class CarListView(LoginRequiredMixin, generic.ListView):
    model = Car
    paginate_by = 5
    ordering = ["model"]


class DriverListView(LoginRequiredMixin, generic.ListView):
    model = Driver
    paginate_by = 5
    ordering = ["username"]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by("username")


class CarDetailView(LoginRequiredMixin, generic.DetailView):
    model = Car


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = Driver
    queryset = Driver.objects.prefetch_related("cars__manufacturer")
