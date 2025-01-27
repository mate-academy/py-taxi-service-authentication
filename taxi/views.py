from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth.decorators import login_required

from .models import Driver, Car, Manufacturer


def index(request):
    """View function for the home page of the site."""

    num_drivers = Driver.objects.count()
    num_cars = Car.objects.count()
    num_manufacturers = Manufacturer.objects.count()

    context = {
        "num_drivers": num_drivers,
        "num_cars": num_cars,
        "num_manufacturers": num_manufacturers,
    }

    return render(request, "taxi/index.html", context=context)


class ManufacturerListView(generic.ListView):
    model = Manufacturer
    context_object_name = "manufacturer_list"
    template_name = "taxi/manufacturer_list.html"
    paginate_by = 5


class CarListView(generic.ListView):
    model = Car
    paginate_by = 5
    queryset = Car.objects.select_related("manufacturer")


class CarDetailView(generic.DetailView):
    model = Car


class DriverListView(generic.ListView):
    model = Driver
    paginate_by = 5


class DriverDetailView(generic.DetailView):
    model = Driver
    queryset = Driver.objects.prefetch_related("cars__manufacturer")


@login_required
def home(request: HttpRequest) -> render:
    if "num_visits" not in request.session:
        request.session["num_visits"] = 0
    request.session["num_visits"] += 1

    num_visits = request.session["num_visits"]

    return render(request, "includes/home.html", {"num_visits": num_visits})


@login_required
def driver_list(request):
    drivers = Driver.objects.all()
    return render(request, "includes/driver_list.html", {"drivers": drivers})


@login_required
def driver_detail(request, ids):
    driver = get_object_or_404(Driver, id=ids)
    return render(request, "includes/driver_detail.html", {"driver": driver})
