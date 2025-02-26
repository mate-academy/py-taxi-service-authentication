from django.contrib.auth import login, logout
from django.urls import path

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
]
