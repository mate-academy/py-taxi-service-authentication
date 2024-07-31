from django.shortcuts import render
from django.views import generic
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from pip._internal.utils import logging
from .models import Car, Driver, Manufacturer


class ManufacturerListView(LoginRequiredMixin, generic.ListView):
    model = Manufacturer
    context_object_name = "manufacturer_list"
    template_name = "taxi/manufacturer_list.html"
    paginate_by = 5


class CarListView(LoginRequiredMixin, generic.ListView):
    model = Car
    paginate_by = 5
    queryset = Car.objects.select_related("manufacturer")
    template_name = "taxi/car_list.html"


class CarDetailView(LoginRequiredMixin, generic.DetailView):
    model = Car
    template_name = "taxi/car_detail.html"


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = Driver
    queryset = Driver.objects.prefetch_related("cars__manufacturer")
    template_name = "taxi/driver_detail.html"


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "taxi/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.session.session_key:
            self.request.session.create()
        num_visits = self.request.session.get("num_visits", 0)
        self.request.session["num_visits"] = num_visits + 1

        context["num_visits"] = num_visits + 1
        context["num_cars"] = Car.objects.count()
        context["num_drivers"] = Driver.objects.count()
        context["num_manufacturers"] = Manufacturer.objects.count()
        return context


class DriverListView(LoginRequiredMixin, ListView):
    model = Driver
    paginate_by = 5
    template_name = "taxi/driver_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_user"] = self.request.user
        return context
