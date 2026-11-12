from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic

from .models import Driver, Car, Manufacturer


@login_required
def index(req):
    """View function for the home page of the site."""

    driver = None
    if req.user.is_authenticated:
        driver = req.user

    num_drivers = Driver.objects.count()
    num_cars = Car.objects.count()
    num_manufacturers = Manufacturer.objects.count()
    num_visits = req.session.get("num_visits", 0)
    num_visits = num_visits + 1
    req.session["num_visits"] = num_visits

    context = {
        "num_drivers": num_drivers,
        "num_cars": num_cars,
        "num_visits": num_visits,
        "num_manufacturers": num_manufacturers,
        "driver": driver,
    }

    return render(req, "taxi/index.html", context=context)


class ManufacturerListView(LoginRequiredMixin, generic.ListView):
    model = Manufacturer
    context_object_name = "manufacturer_list"
    template_name = "taxi/manufacturer_list.html"
    paginate_by = 5


class CarListView(LoginRequiredMixin, generic.ListView):
    model = Car
    paginate_by = 5
    queryset = Car.objects.select_related("manufacturer")


class CarDetailView(LoginRequiredMixin, generic.DetailView):
    model = Car


class DriverListView(LoginRequiredMixin, generic.ListView):
    model = Driver
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_user"] = self.request.user
        return context


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = Driver
    queryset = Driver.objects.prefetch_related("cars__manufacturer")
