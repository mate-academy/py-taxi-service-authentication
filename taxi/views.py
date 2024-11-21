from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views import generic
from .models import Driver, Car, Manufacturer


def index(request):
    if not request.user.is_authenticated:
        return redirect("taxi:login")

    num_drivers = Driver.objects.count()
    num_cars = Car.objects.count()
    num_manufacturers = Manufacturer.objects.count()

    if "num_visits" not in request.session:
        request.session["num_visits"] = 1
    else:
        request.session["num_visits"] += 1

    num_visits = request.session["num_visits"]

    context = {
        "num_drivers": num_drivers,
        "num_cars": num_cars,
        "num_manufacturers": num_manufacturers,
        "num_visits": num_visits,
    }

    return render(request, "taxi/index.html", context=context)


@login_required
def driver_detail(request, pk):
    driver = Driver.objects.get(pk=pk)
    return render(request, "taxi/driver_detail.html", {"driver": driver})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("taxi:index")
    else:
        form = AuthenticationForm()

    return render(request, "taxi/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("taxi:index")


class ManufacturerListView(generic.ListView):
    model = Manufacturer
    context_object_name = "manufacturer_list"
    template_name = "taxi/manufacturer_list.html"
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("taxi:login")
        return super().get(request, *args, **kwargs)


class CarListView(generic.ListView):
    model = Car
    paginate_by = 5
    queryset = Car.objects.select_related("manufacturer").order_by("id")

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("taxi:login")
        return super().get(request, *args, **kwargs)


class CarDetailView(generic.DetailView):
    model = Car

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("taxi:login")
        return super().get(request, *args, **kwargs)


class DriverListView(generic.ListView):
    model = Driver
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("taxi:login")
        return super().get(request, *args, **kwargs)


class DriverDetailView(generic.DetailView):
    model = Driver
    queryset = Driver.objects.prefetch_related("cars__manufacturer")

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("taxi:login")
        return super().get(request, *args, **kwargs)
