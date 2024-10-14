from django.views import View, generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Driver, Car, Manufacturer
from django.shortcuts import render


@login_required
def index(request):
    if "num_visits" in request.session:
        request.session["num_visits"] += 1
    else:
        request.session["num_visits"] = 1

    return render(request, "taxi/index.html", {
        "num_visits": request.session["num_visits"],
    })


def get(request):
    num_drivers = Driver.objects.count()
    num_cars = Car.objects.count()
    num_manufacturers = Manufacturer.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_drivers": num_drivers,
        "num_cars": num_cars,
        "num_manufacturers": num_manufacturers,
        "num_visits": num_visits,
    }

    return render(request, "taxi/index.html", context=context)


@method_decorator(login_required, name="dispatch")
class IndexView(View):
    """Class-based view for the home page of the site."""


@method_decorator(login_required, name="dispatch")
class ManufacturerListView(generic.ListView):
    model = Manufacturer
    context_object_name = "manufacturer_list"
    template_name = "taxi/manufacturer_list.html"
    paginate_by = 5


@method_decorator(login_required, name="dispatch")
class CarListView(generic.ListView):
    model = Car
    paginate_by = 5
    queryset = Car.objects.select_related("manufacturer")


@method_decorator(login_required, name="dispatch")
class CarDetailView(generic.DetailView):
    model = Car


@method_decorator(login_required, name="dispatch")
class DriverListView(generic.ListView):
    model = Driver
    paginate_by = 5

    def get_context_data(self, object_list=None, **kwargs):
        context = super(DriverListView, self).get_context_data(**kwargs)
        context["current_user"] = self.request.user
        return context


@method_decorator(login_required, name="dispatch")
class DriverDetailView(generic.DetailView):
    model = Driver
    queryset = Driver.objects.prefetch_related("cars__manufacturer")
