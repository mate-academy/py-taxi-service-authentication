from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Driver, Car, Manufacturer


@login_required
def index(request):
    num_visits = request.session.get("num_visits", 0) + 1
    request.session["num_visits"] = num_visits
    context = {
        "num_visits": num_visits,
        "num_drivers": Driver.objects.count(),
        "num_cars": Car.objects.count(),
        "num_manufacturers": Manufacturer.objects.count(),
    }
    return render(request, "taxi/index.html", context)


class DriverListView(LoginRequiredMixin, ListView):
    model = Driver
    template_name = "taxi/driver_list.html"
    context_object_name = "driver_list"

    def get_queryset(self):
        queryset = super().get_queryset()
        for driver in queryset:
            if driver.user == self.request.user:
                driver.username += " (Me)"
        return queryset


class DriverDetailView(LoginRequiredMixin, DetailView):
    model = Driver
    template_name = "taxi/driver_detail.html"
    context_object_name = "driver"
