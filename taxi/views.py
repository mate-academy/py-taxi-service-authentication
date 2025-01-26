from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import generic
from .models import Driver, Car, Manufacturer


@login_required()
def index(request):
    """View function for the home page of the site."""
    request.session["num_visits"] = request.session.get("num_visits", 0) + 1
    num_drivers = Driver.objects.count()
    num_cars = Car.objects.count()
    num_manufacturers = Manufacturer.objects.count()

    context = {
        "num_drivers": num_drivers,
        "num_cars": num_cars,
        "num_manufacturers": num_manufacturers,
        "num_visits": request.session["num_visits"]
    }

    return render(request, "taxi/index.html", context=context)


class ManufacturerListView(generic.ListView, LoginRequiredMixin):
    model = Manufacturer
    context_object_name = "manufacturer_list"
    template_name = "taxi/manufacturer_list.html"
    paginate_by = 5


class CarListView(generic.ListView, LoginRequiredMixin):
    model = Car
    paginate_by = 5
    queryset = Car.objects.select_related("manufacturer")


class CarDetailView(generic.DetailView, LoginRequiredMixin):
    model = Car


class DriverListView(generic.ListView, LoginRequiredMixin):
    model = Driver
    paginate_by = 5


class DriverDetailView(generic.DetailView, LoginRequiredMixin):
    model = Driver
    queryset = Driver.objects.prefetch_related("cars__manufacturer")
