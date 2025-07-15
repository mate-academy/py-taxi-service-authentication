from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy

from .models import Driver, Car, Manufacturer


@login_required
def index(request):
    """View function for the home page of the site."""

    # Visit counter logic
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    num_drivers = Driver.objects.count()
    num_cars = Car.objects.count()
    num_manufacturers = Manufacturer.objects.count()

    context = {
        'num_drivers': num_drivers,
        'num_cars': num_cars,
        'num_manufacturers': num_manufacturers,
        'num_visits': num_visits + 1,
    }

    return render(request, 'taxi/index.html', context=context)


class ManufacturerListView(LoginRequiredMixin, generic.ListView):
    model = Manufacturer
    context_object_name = 'manufacturer_list'
    template_name = 'taxi/manufacturer_list.html'
    paginate_by = 5


class ManufacturerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Manufacturer
    template_name = 'taxi/manufacturer_detail.html'


class CarListView(LoginRequiredMixin, generic.ListView):
    model = Car
    paginate_by = 5
    queryset = Car.objects.select_related('manufacturer')


class CarDetailView(LoginRequiredMixin, generic.DetailView):
    model = Car


class DriverListView(LoginRequiredMixin, generic.ListView):
    model = Driver
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_user'] = self.request.user
        return context


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = Driver
