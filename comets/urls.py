from django.urls import path, register_converter

from comets import views, converters

app_name = "comets"

register_converter(converters.DateConverter, "dateiso")

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("lost/", views.LostView.as_view(), name="lost"),
    path("comets/", views.CometsListView.as_view(), name="list"),
    path("comets/<int:id>/<dateiso:date_ref>", views.CometDetailView.as_view(), name="detail")
]