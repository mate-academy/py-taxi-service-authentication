<<<<<<< HEAD
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
=======
from django.contrib.auth.mixins import LoginRequiredMixin
>>>>>>> 9ec6aba500bb01d17ec55bca21b477b65d9d5c38
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.decorators import login_required

from .models import Driver, Car, Manufacturer


@login_required
def index(request):
<<<<<<< HEAD
    if "num_visits" not in request.session:
        request.session["num_visits"] = 0

    request.session["num_visits"] += 1

=======
>>>>>>> 9ec6aba500bb01d17ec55bca21b477b65d9d5c38
    num_drivers = Driver.objects.count()
    num_cars = Car.objects.count()
    num_manufacturers = Manufacturer.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_drivers": num_drivers,
        "num_cars": num_cars,
        "num_manufacturers": num_manufacturers,
<<<<<<< HEAD
        "num_visits": request.session["num_visits"],
=======
        "num_visits": num_visits,
>>>>>>> 9ec6aba500bb01d17ec55bca21b477b65d9d5c38
    }

    return render(request, "taxi/index.html", context)


class ManufacturerListView(LoginRequiredMixin, generic.ListView):
    model = Manufacturer
    context_object_name = "manufacturer_list"
    template_name = "taxi/manufacturer_list.html"
    paginate_by = 5


class CarListView(LoginRequiredMixin, generic.ListView):
    model = Car
    paginate_by = 5
    queryset = Car.objects.select_related("manufacturer").order_by("id")


class CarDetailView(LoginRequiredMixin, generic.DetailView):
    model = Car


class DriverListView(LoginRequiredMixin, generic.ListView):
    model = Driver
    paginate_by = 5


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = Driver
    queryset = Driver.objects.prefetch_related("cars__manufacturer")
