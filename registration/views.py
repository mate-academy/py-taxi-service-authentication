from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

# Create your views here.
def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('taxi:index'))
        else:
            context = {
                'message': 'Invalid username or password.',
            }
            return render(request, "registration/login.html", context=context)
    if request.method == 'GET':
        return render(request, "registration/login.html")

def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return render(request, 'registration/logout.html')