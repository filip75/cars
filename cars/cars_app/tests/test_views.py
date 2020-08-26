from json import loads
from unittest.mock import patch

from django.urls import reverse
from rest_framework.test import APIRequestFactory, APITestCase

from cars_app.models import Car, CarRate
from cars_app.views import (
    CarSerializer,
    CreateCarRateView,
    ListCreateCarsView,
    ListTopCarView,
)


class CarSerializerTest(APITestCase):
    def test_car_doesnt_exist(self):
        with patch("cars_app.views.vehicle_exists") as api_patch:
            api_patch.return_value = False

            serializer = CarSerializer(data={"make": "car_make", "model": "car_model"})

            self.assertFalse(serializer.is_valid())

    def test_car_exists(self):
        with patch("cars_app.views.vehicle_exists") as api_patch:
            api_patch.return_value = True

            serializer = CarSerializer(data={"make": "car_make", "model": "car_model"})

            self.assertTrue(serializer.is_valid())


class ListCreateCarsViewTest(APITestCase):
    def setUp(self):
        self.view = ListCreateCarsView.as_view()
        self.factory = APIRequestFactory()
        Car.objects.create(id=1, make="Honda", model="Civic")
        fiat = Car.objects.create(id=2, make="Fiat", model="500")
        CarRate.objects.bulk_create(
            [
                CarRate(car=fiat, value=1),
                CarRate(car=fiat, value=2),
                CarRate(car=fiat, value=4),
            ]
        )

        self.expected = [
            {"id": 1, "make": "Honda", "model": "Civic", "avarage_rate": None},
            {"id": 2, "make": "Fiat", "model": "500", "avarage_rate": 2.33},
        ]

    def test_returns_correct_data(self):
        request = self.factory.get(reverse("cars_app_cars"))

        response = self.view(request)
        response.render()

        self.assertEqual(response.status_code, 200)
        self.assertEqual((loads(response.content)["results"]), self.expected)

    def test_create_car(self):
        self.assertFalse(Car.objects.filter(id=3).exists())
        request = self.factory.post(
            reverse("cars_app_cars"), {"make": "Fiat", "model": "Tipo"}
        )

        with patch("cars_app.views.vehicle_exists") as api_patch:
            api_patch.return_value = True
            response = self.view(request)

        self.assertEqual(response.status_code, 201)
        self.assertTrue(Car.objects.filter(id=3).exists())


class CreateCarRateViewTest(APITestCase):
    def setUp(self):
        self.view = CreateCarRateView.as_view()
        self.factory = APIRequestFactory()
        self.car = Car.objects.create(make="Honda", model="Civic")

    def test_create_rate(self):
        self.assertFalse(CarRate.objects.filter(car=self.car).exists())
        request = self.request = self.factory.post(
            reverse("cars_app_rates"), {"car": self.car.id, "value": 2}
        )

        response = self.view(request)

        self.assertEqual(response.status_code, 201)
        self.assertTrue(CarRate.objects.filter(car=self.car, value=2).exists())

    def test_incorrect_rate(self):
        request1 = self.request = self.factory.post(
            reverse("cars_app_rates"), {"car": self.car.id, "value": 6}
        )
        request2 = self.request = self.factory.post(
            reverse("cars_app_rates"), {"car": self.car.id, "value": 0}
        )

        response1 = self.view(request1)
        response2 = self.view(request2)

        self.assertEqual(response1.status_code, 400)
        self.assertEqual(response2.status_code, 400)


class ListTopCarViewTest(APITestCase):
    def setUp(self):
        self.view = ListTopCarView.as_view()
        self.factory = APIRequestFactory()

        self.car1 = Car.objects.create(id=1, make="Honda", model="Civic")
        self.car2 = Car.objects.create(id=2, make="Fiat", model="500")
        self.car3 = Car.objects.create(id=3, make="Fiat", model="Tipo")

        CarRate.objects.bulk_create(
            [
                CarRate(car=self.car1, value=1),
                CarRate(car=self.car1, value=1),
                CarRate(car=self.car2, value=1),
                CarRate(car=self.car2, value=1),
                CarRate(car=self.car2, value=1),
            ]
        )

        self.expected = [
            {"id": 2, "make": "Fiat", "model": "500", "votes": 3},
            {"id": 1, "make": "Honda", "model": "Civic", "votes": 2},
            {"id": 3, "make": "Fiat", "model": "Tipo", "votes": 0},
        ]

    def test_returns_correct_data(self):
        request = self.factory.get(reverse("cars_app_top"))

        response = self.view(request)
        response.render()

        self.assertEqual(loads(response.content)["results"], self.expected)
