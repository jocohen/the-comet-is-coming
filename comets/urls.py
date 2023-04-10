from django.urls import path

from . import views

app_name = "comets"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("lost/", views.LostView.as_view(), name="lost"),
]