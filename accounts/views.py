from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from taxi.models import Driver


@login_required
def login_view(request):
    return HttpResponse


@login_required
def driver_list(request):
    drivers = Driver.objects.all()
    context = {
        "drivers": drivers,
        "current_user": request.user,
    }
    return render(request, "drivers/driver_list.html", context)
