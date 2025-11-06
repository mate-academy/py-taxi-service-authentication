from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.shortcuts import render
from .models import Driver, Car, Manufacturer


@login_required
def index(request):
    """View da página inicial, com contador de visitas."""
    num_drivers = Driver.objects.count()
    num_cars = Car.objects.count()
    num_manufacturers = Manufacturer.objects.count()

    # contador de visitas na sessão
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_drivers": num_drivers,
        "num_cars": num_cars,
        "num_manufacturers": num_manufacturers,
        "num_visits": num_visits,
    }
    return render(request, "taxi/index.html", context)


# --------- MANUFACTURER ---------

class ManufacturerListView(LoginRequiredMixin, generic.ListView):
    model = Manufacturer
    paginate_by = 10


class ManufacturerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Manufacturer


# --------- CAR ---------

class CarListView(LoginRequiredMixin, generic.ListView):
    model = Car
    paginate_by = 10


class CarDetailView(LoginRequiredMixin, generic.DetailView):
    model = Car


# --------- DRIVER ---------

class DriverListView(LoginRequiredMixin, generic.ListView):
    model = Driver
    paginate_by = 10
    template_name = "taxi/driver_list.html"

    def get_queryset(self):
        return Driver.objects.select_related("user").all()

    def get_context_data(self, **kwargs):
        """Adiciona o usuário logado ao contexto para comparar com os motoristas."""
        context = super().get_context_data(**kwargs)
        context["current_user"] = self.request.user
        return context


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = Driver
    template_name = "taxi/driver_detail.html"
