from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic

from taxi.models import Manufacturer, Car, Driver


@login_required
def index(request):
    num_manufacturers = Manufacturer.objects.count()
    num_cars = Car.objects.count()
    num_drivers = Driver.objects.count()

    request.session["num_visits"] = (
        request.session.get("num_visits", 0) + 1
    )

    context = {
        "num_manufacturers": num_manufacturers,
        "num_cars": num_cars,
        "num_drivers": num_drivers,
        "num_visits": request.session["num_visits"],
    }

    return render(request, "taxi/index.html", context=context)


class ManufacturerListView(LoginRequiredMixin, generic.ListView):
    model = Manufacturer
    paginate_by = 5


class ManufacturerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Manufacturer


class CarListView(LoginRequiredMixin, generic.ListView):
    model = Car
    paginate_by = 5


class CarDetailView(LoginRequiredMixin, generic.DetailView):
    model = Car


class DriverListView(LoginRequiredMixin, generic.ListView):
    model = Driver
    paginate_by = 5


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = Driver
