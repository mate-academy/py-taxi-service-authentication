from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from taxi.models import Car, Driver, Manufacturer


class ManufacturerListView(LoginRequiredMixin, ListView):
    """Display a paginated list of all manufacturers ordered by name."""

    model = Manufacturer
    queryset: QuerySet = Manufacturer.objects.order_by("name")
    paginate_by: int = 5
    template_name: str = "taxi/manufacturer_list.html"
    context_object_name: str = "manufacturer_list"


class CarListView(LoginRequiredMixin, ListView):
    """Display a paginated list of cars with manufacturer preloaded."""

    model = Car
    queryset: QuerySet = Car.objects.select_related("manufacturer")
    paginate_by: int = 5
    template_name: str = "taxi/car_list.html"
    context_object_name: str = "car_list"


class CarDetailView(LoginRequiredMixin, DetailView):
    """Display detail information for a single car."""

    model = Car
    template_name: str = "taxi/car_detail.html"


class DriverListView(LoginRequiredMixin, ListView):
    """Display a paginated list of all drivers."""

    model = Driver
    paginate_by: int = 5
    template_name: str = "taxi/driver_list.html"
    context_object_name: str = "driver_list"


class DriverDetailView(LoginRequiredMixin, DetailView):
    """Display detail information for a single driver with their cars."""

    model = Driver
    queryset: QuerySet = Driver.objects.prefetch_related(
        "cars__manufacturer"
    )
    template_name: str = "taxi/driver_detail.html"


@login_required
def index(request):
    """Render the home page with summary counts and visit counter."""
    num_drivers = Driver.objects.count()
    num_cars = Car.objects.count()
    num_manufacturers = Manufacturer.objects.count()

    num_visits = request.session.get("num_visits", 0) + 1
    request.session["num_visits"] = num_visits

    context = {
        "num_drivers": num_drivers,
        "num_cars": num_cars,
        "num_manufacturers": num_manufacturers,
        "num_visits": num_visits,
    }
    return render(request, "taxi/index.html", context=context)
