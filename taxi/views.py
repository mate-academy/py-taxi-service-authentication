from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.shortcuts import render
from .models import Driver, Car, Manufacturer


@login_required
def index(request):
  """Página inicial com contador de visitas e estatísticas."""
  num_drivers = Driver.objects.count()
  num_cars = Car.objects.count()
  num_manufacturers = Manufacturer.objects.count()

  # Incrementar o contador antes de renderizar (corrigido)
  num_visits = request.session.get("num_visits", 0) + 1
  request.session["num_visits"] = num_visits

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
  template_name = "taxi/manufacturer_list.html"


class ManufacturerDetailView(LoginRequiredMixin, generic.DetailView):
  model = Manufacturer
  template_name = "taxi/manufacturer_detail.html"


# --------- CAR ---------

class CarListView(LoginRequiredMixin, generic.ListView):
  model = Car
  paginate_by = 10
  template_name = "taxi/car_list.html"


class CarDetailView(LoginRequiredMixin, generic.DetailView):
  model = Car
  template_name = "taxi/car_detail.html"


# --------- DRIVER ---------

class DriverListView(LoginRequiredMixin, generic.ListView):
  model = Driver
  paginate_by = 10
  template_name = "taxi/driver_list.html"

  def get_queryset(self):
    """Usa select_related para otimizar o acesso ao usuário vinculado."""
    return Driver.objects.select_related("user").all()

  def get_context_data(self, **kwargs):
    """Adiciona o usuário logado ao contexto para identificar 'Eu'."""
    context = super().get_context_data(**kwargs)
    context["current_user"] = self.request.user
    return context


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
  model = Driver
  template_name = "taxi/driver_detail.html"
