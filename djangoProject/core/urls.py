from django.urls import path

from core.views import PersonListView, PersonCreateView

urlpatterns = [
    path("people/", PersonListView.as_view(), name="person-list"),
    path("people/create/", PersonCreateView.as_view(), name="person-create"),
]

app_name = "core"
