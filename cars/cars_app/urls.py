from django.urls import path

from cars_app.views import ListCreateCarsView, CreateCarRateView, ListTopCarView

urlpatterns = [
    path("cars/", ListCreateCarsView.as_view()),
    path("rate/", CreateCarRateView.as_view()),
    path("top/", ListTopCarView.as_view()),
]
