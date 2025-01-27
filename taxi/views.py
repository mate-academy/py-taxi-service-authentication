from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
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


def login_view(request: HttpRequest) -> HttpResponse:
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
                "error": "Invalid username or password"}
        return HttpResponse("Login", context=error_context)


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return render(request, "accounts/logged_out.html")

"""    user = getattr(request, "user", None)
    if not getattr(user, "is_authenticated", True):
        user = None
    user_logged_out.send(sender=user.__class__, request=request, user=user)
    request.session.flush()
    if hasattr(request, "user"):
        from django.contrib.auth.models import AnonymousUser

        request.user = AnonymousUser()"""


@login_required
def home(request):
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1
    return render(
        request,
        "base.html",
        {"num_visits": num_visits}
    )


@login_required
def driver_list(request):
    drivers = Driver.objects.all()
    return render(
        request,
        "taxi/driver_list.html",
        {"drivers": drivers, "current_user": request.user}
    )


@login_required
def driver_list(request):
    drivers = Driver.objects.all()
    return render(
        request,
        "taxi/driver_list.html",
        {"drivers": drivers, "current_user": request.user}
    )
