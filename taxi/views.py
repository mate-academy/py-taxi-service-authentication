from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.shortcuts import render
from django.views import generic

from .models import Driver, Car, Manufacturer


@login_required
def index(request):
    """View function for the home page of the site with visit counter."""
    num_visits = request.session.get("num_visits", 0) + 1
    request.session["num_visits"] = num_visits

    context = {
        "num_visits": num_visits,
        "num_drivers": Driver.objects.count(),
        "num_cars": Car.objects.count(),
        "num_manufacturers": Manufacturer.objects.count(),
    }

    return render(request, "taxi/index.html", context=context)


class ManufacturerListView(LoginRequiredMixin, generic.ListView):
    model = Manufacturer
    ordering = ["name"]
    paginate_by = 5
    context_object_name = "manufacturer_list"
    template_name = "taxi/manufacturer_list.html"


class CarListView(LoginRequiredMixin, generic.ListView):
    model = Car
    queryset = Car.objects.select_related("manufacturer").order_by("id")
    paginate_by = 5
    context_object_name = "car_list"
    template_name = "taxi/car_list.html"


class CarDetailView(LoginRequiredMixin, generic.DetailView):
    model = Car
    template_name = "taxi/car_detail.html"
    context_object_name = "car"


class DriverListView(LoginRequiredMixin, generic.ListView):
    model = Driver
    paginate_by = 5
    context_object_name = "driver_list"
    template_name = "taxi/driver_list.html"


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = Driver
    queryset = Driver.objects.prefetch_related(
        Prefetch("cars", queryset=Car.objects.select_related("manufacturer"))
    )
    context_object_name = "driver"
    template_name = "taxi/driver_detail.html"
