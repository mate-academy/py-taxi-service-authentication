from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from taxi.models import Driver, Car, Manufacturer


@login_required(login_url="login")
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
        "num_visits": num_visits + 1,
    }

    return render(request, "taxi/index.html", context=context)


class ManufacturerListView(LoginRequiredMixin, generic.ListView):
    model = Manufacturer
    context_object_name = "manufacturer_list"
    template_name = "taxi/manufacturer_list.html"
    paginate_by = 5
    login_url = "login"


class CarListView(LoginRequiredMixin, generic.ListView):
    model = Car
    paginate_by = 5
    queryset = Car.objects.select_related("manufacturer")
    login_url = "login"


class CarDetailView(LoginRequiredMixin, generic.DetailView):
    model = Car
    login_url = "login"


class DriverListView(LoginRequiredMixin, generic.ListView):
    model = Driver
    paginate_by = 5
    login_url = "login"


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = Driver
    queryset = Driver.objects.prefetch_related("cars__manufacturer")
    login_url = "login"


# my text
def test_session_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse(
        "<h1>Test session</h1>"
        f"<h2>Session data: {request.session['test']}</h2>"
    )
