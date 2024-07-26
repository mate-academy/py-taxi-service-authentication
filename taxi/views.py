from venv import logger

from django.shortcuts import render
from django.views import generic
from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Car, Driver, Manufacturer


def index(request):
    """View function for the home page of the site."""

    num_drivers = Driver.objects.count()
    num_cars = Car.objects.count()
    num_manufacturers = Manufacturer.objects.count()
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_drivers": num_drivers,
        "num_cars": num_cars,
        "num_manufacturers": num_manufacturers,
        "num_visits": num_visits,
    }

    return render(request, "taxi/index.html", context=context)


class ManufacturerListView(LoginRequiredMixin, generic.ListView):
    model = Manufacturer
    context_object_name = "manufacturer_list"
    template_name = "taxi/manufacturer_list.html"
    paginate_by = 5


class CarListView(LoginRequiredMixin, generic.ListView):
    model = Car
    paginate_by = 5
    queryset = Car.objects.select_related("manufacturer")
    template_name = "taxi/car_list.html"


class CarDetailView(LoginRequiredMixin, generic.DetailView):
    model = Car
    template_name = "taxi/car_detail.html"


class DriverListView(LoginRequiredMixin, generic.ListView):
    model = Driver
    paginate_by = 5
    template_name = "taxi/driver_list.html"


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = Driver
    queryset = Driver.objects.prefetch_related("cars__manufacturer")
    emplate_name = "taxi/driver_detail.html"


@login_required
def home(request):

    if not request.session.session_key:
        request.session.create()
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1
    logger.debug(f'num_visits: {num_visits + 1}')  # Добавить логирование
    return render(request, "taxi/index.html", {"num_visits": num_visits + 1})


@login_required
def driver_list(request):
    drivers = Driver.objects.all()
    current_user = request.user
    return render(
        request, "taxi/driver_list.html",
        {"drivers": drivers, "current_user": current_user}
    )
