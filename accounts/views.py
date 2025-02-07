from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render


def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        return render(request, "registration/login.html")
    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect("taxi/index.html")
        else:
            error_context = {
                "error": "Invalid Credentials",
            }
            return render(request, "registration/login.html", error_context)


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return HttpResponseRedirect("registration/logged_out.html")
