from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView

from taxi.models import Car, Driver, Manufacturer


@login_required
def index(request):
    num_visits = request.session.get("num_visits", 0) + 1
    request.session["num_visits"] = num_visits

    num_drivers = Driver.objects.count()
    num_cars = Car.objects.count()
    num_manufacturers = Manufacturer.objects.count()

    context = {
        "num_drivers": num_drivers,
        "num_cars": num_cars,
        "num_manufacturers": num_manufacturers,
        "num_visits": num_visits,
    }
    return render(request, "taxi/index.html", context)


@method_decorator(login_required, name="dispatch")
class ManufacturerListView(ListView):
    model = Manufacturer
    queryset = Manufacturer.objects.all().order_by("name")
    paginate_by = 5


@method_decorator(login_required, name="dispatch")
class CarListView(ListView):
    model = Car
    paginate_by = 5
    queryset = Car.objects.select_related("manufacturer").all()


@method_decorator(login_required, name="dispatch")
class CarDetailView(DetailView):
    model = Car


@method_decorator(login_required, name="dispatch")
class DriverListView(ListView):
    model = Driver
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_user_id"] = self.request.user.id
        return context


@method_decorator(login_required, name="dispatch")
class DriverDetailView(DetailView):
    model = Driver
    queryset = Driver.objects.prefetch_related(
        Prefetch(
            "cars",
            queryset=Car.objects.select_related("manufacturer"),
        )
    )
