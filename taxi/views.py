from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.views.generic import TemplateView

from .models import Driver, Car, Manufacturer


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "taxi/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        num_visits = self.request.session.get("num_visits", 0) + 1
        self.request.session["num_visits"] = num_visits

        context["num_visits"] = num_visits
        return context


class ManufacturerListView(LoginRequiredMixin, generic.ListView):
    model = Manufacturer
    paginate_by = 5


class CarListView(LoginRequiredMixin, generic.ListView):
    model = Car
    paginate_by = 5
    queryset = Car.objects.select_related("manufacturer")


class CarDetailView(LoginRequiredMixin, generic.DetailView):
    model = Car


class DriverListView(LoginRequiredMixin, generic.ListView):
    model = Driver
    paginate_by = 5


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = Driver
    queryset = Driver.objects.prefetch_related("cars__manufacturer")
