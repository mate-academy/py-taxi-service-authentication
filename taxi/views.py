from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import Driver, Car, Manufacturer


@login_required
def index(request):
    num_visits = request.session.get("num_visits", 0)
    num_visits += 1
    request.session["num_visits"] = num_visits

    context = {
        "num_visits": num_visits,
    }
    return render(request, "taxi/index.html", context)


class ManufacturerListView(LoginRequiredMixin, generic.ListView):
    model = Manufacturer
    context_object_name = "manufacturer_list"
    template_name = "taxi/manufacturer_list.html"
    queryset = Manufacturer.objects.order_by("name")
    paginate_by = 5


class CarListView(LoginRequiredMixin, generic.ListView):
    model = Car
    context_object_name = "car_list"
    paginate_by = 5

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("manufacturer")
            .order_by("model")
        )


class DriverListView(LoginRequiredMixin, generic.ListView):
    model = Driver
    context_object_name = "driver_list"
    paginate_by = 5

    def get_queryset(self):
        return super().get_queryset().order_by("username")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_driver"] = self.request.user
        return context


class CarDetailView(LoginRequiredMixin, generic.DetailView):
    model = Car
    context_object_name = "car"


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = Driver
    context_object_name = "driver"
    queryset = Driver.objects.prefetch_related("cars__manufacturer")
