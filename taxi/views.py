from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic

import taxi
from .models import Driver, Car, Manufacturer

@login_required
def index(request):
    """View function for the home page of the site."""

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


class RegisterForm:
    pass


def user_login(request) -> HttpResponse:
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        form = RegisterForm(request.POST)
        if user:
            login(request, user)
            return redirect(reverse("taxi:index"))
        else:
            error_context ={
                "error": "Invalid credenticals."
            }
            return render(request, "registration/login.html", context=error_context)

def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return render(request, "registration/logout.html")
