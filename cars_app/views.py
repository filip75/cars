from rest_framework.generics import ListCreateAPIView, CreateAPIView, ListAPIView
from rest_framework import serializers
from cars_app.models import Car, CarRate
from django.db.models import Avg, Count
from cars_app.vehicle_api import vehicle_exists
from rest_framework.exceptions import ValidationError


class CarSerializer(serializers.ModelSerializer):
    avarage_rate = serializers.FloatField(read_only=True)

    def validate(self, attrs):
        if not vehicle_exists(attrs["make"], attrs["model"]):
            raise ValidationError("Car doesn't exist")
        return attrs

    class Meta:
        model = Car
        fields = ["id", "make", "model", "avarage_rate"]
        read_only_fields = ["id", "avarage_rate"]


class ListCreateCarsView(ListCreateAPIView):
    serializer_class = CarSerializer
    queryset = Car.objects.annotate(avarage_rate=Avg("rates__value")).all()


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarRate
        fields = ["car", "value"]


class CreateCarRateView(CreateAPIView):
    serializer_class = RateSerializer
    queryset = CarRate.objects.all()


class TopCarsSerializer(serializers.ModelSerializer):
    votes = serializers.IntegerField()
    class Meta:
        model = Car
        fields = ["id", "make", "model", "votes"]


class ListTopCarView(ListAPIView):
    serializer_class = TopCarsSerializer
    queryset = Car.objects.annotate(votes=Count("rates")).order_by("-votes").all()
