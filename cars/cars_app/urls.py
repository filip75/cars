from django.urls import path

from cars_app.views import CreateCarRateView, ListCreateCarsView, ListTopCarView

urlpatterns = [
    path("cars/", ListCreateCarsView.as_view(), name="cars_app_cars"),
    path("rate/", CreateCarRateView.as_view(), name="cars_app_rates"),
    path("top/", ListTopCarView.as_view(), name="cars_app_top"),
]
