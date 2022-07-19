from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic

from .models import Driver, Car, Manufacturer


@login_required
def index(request):
    num_drivers = Driver.objects.count()
    num_cars = Car.objects.count()
    num_manufacturers = Manufacturer.objects.count()
    num_visit = request.session.get("num_visit", 0)
    request.session["num_visit"] = num_visit + 1

    context = {
        "num_drivers": num_drivers,
        "num_cars": num_cars,
        "num_manufacturers": num_manufacturers,
        "num_visit": num_visit + 1,
    }

    return render(request, "taxi/index.html", context=context)


class ManufacturerListView(LoginRequiredMixin, generic.ListView):
    model = Manufacturer
    paginate_by = 2
    queryset = Manufacturer.objects.all().order_by("name")


class CarListView(LoginRequiredMixin, generic.ListView):
    model = Car
    paginate_by = 2
    queryset = Car.objects.all().select_related("manufacturer").order_by("model")


class DriverListView(LoginRequiredMixin, generic.ListView):
    model = Driver
    paginate_by = 2


class CarDetailView(LoginRequiredMixin, generic.DetailView):
    model = Car


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = Driver
    queryset = Driver.objects.prefetch_related("cars")
