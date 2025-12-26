from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import redirect, render, resolve_url
from django.utils.encoding import iri_to_uri
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.translation import gettext as _
from django.views import generic

from taxi.models import Car, Driver, Manufacturer


class PostRedirectGetLoginView(LoginView):
    template_name = "registration/login.html"

    def resolve_safe_redirect_target(self) -> str | None:
        target = (
            self.request.POST.get(REDIRECT_FIELD_NAME)
            or self.request.GET.get(REDIRECT_FIELD_NAME)
        )
        if not target:
            return None
        if url_has_allowed_host_and_scheme(
                target,
                allowed_hosts={self.request.get_host()},
                require_https=self.request.is_secure(),
        ):
            return target
        return None

    def form_invalid(self, form) -> HttpResponse:
        messages.error(self.request, _("Invalid username or password."))
        self.request.session["has_login_error"] = True

        current_url = iri_to_uri(resolve_url(self.request.path))
        redirect_target = self.resolve_safe_redirect_target()
        if redirect_target:
            query = urlencode({REDIRECT_FIELD_NAME: redirect_target})
            return redirect(f"{current_url}?{query}")
        return redirect(current_url)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["has_login_error"] = self.request.session.pop(
            "has_login_error",
            False,
        )
        return context


@login_required
def index(request):
    num_drivers = Driver.objects.count()
    num_cars = Car.objects.count()
    num_manufacturers = Manufacturer.objects.count()

    num_visits = request.session.get("num_visits", 0) + 1
    request.session["num_visits"] = num_visits

    context = {
        "num_drivers": num_drivers,
        "num_cars": num_cars,
        "num_manufacturers": num_manufacturers,
        "num_visits": num_visits,
    }
    return render(request, "taxi/index.html", context=context)


class ManufacturerListView(LoginRequiredMixin, generic.ListView):
    model = Manufacturer
    paginate_by = 5


class CarListView(LoginRequiredMixin, generic.ListView):
    model = Car
    paginate_by = 5
    queryset = (
        Car.objects
        .select_related("manufacturer")
        .annotate(num_drivers=Count("drivers", distinct=True))
        .order_by("model", "id")
    )


class CarDetailView(LoginRequiredMixin, generic.DetailView):
    model = Car
    queryset = (
        Car.objects
        .select_related("manufacturer")
        .prefetch_related("drivers")
        .annotate(driver_count=Count("drivers", distinct=True))
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["drivers"] = self.object.drivers.all()
        return context


class DriverListView(LoginRequiredMixin, generic.ListView):
    model = Driver
    paginate_by = 5


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = Driver
    queryset = Driver.objects.prefetch_related("cars__manufacturer")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cars"] = self.object.cars.all()
        return context
