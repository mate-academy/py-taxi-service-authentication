from django.views import generic
from django.urls import reverse_lazy
from django.views.generic import ListView

from core.forms import PersonForm
from core.models import Person

# Create your views here.


class PersonListView(ListView):
    model = Person


class PersonCreateView(generic.CreateView):
    model = Person
    success_url = reverse_lazy("core:person-list")
    template_name = "core/person_form.html"
    form_class = PersonForm


