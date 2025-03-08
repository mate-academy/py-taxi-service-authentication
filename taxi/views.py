from http.client import HTTPResponse

from django.shortcuts import render
from django.views import generic
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

from .models import Driver, Car, Manufacturer


def index(request):
    """View function for the home page of the site."""

    num_visits = request.session.get("num_visits", 0) + 1
    request.session["num_visits"] = num_visits

    num_drivers = Driver.objects.count()
    num_cars = Car.objects.count()
    num_manufacturers = Manufacturer.objects.count()

    context = {
        "num_drivers": num_drivers,
        "num_cars": num_cars,
        "num_manufacturers": num_manufacturers,
        "num_visits": num_visits
    }

    return render(request, "taxi/index.html", context=context)


def login_view(request: HttpRequest) -> HTTPResponse:
    if request.method == "GET":
        return render(request, "accounts/login.html")
    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("taxi:index"))
        else:
            error_context = {
               "error": "Invalid credential"
            }
            return  render(request, "accounts/login.html", context=error_context)


def logout_view(request: HttpRequest) -> HTTPResponse:
    logout(request)
    return  render(request, "accounts/logged_out.html")


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
