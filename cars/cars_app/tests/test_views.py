from cars_app.models import Car
from rest_framework.test import APITestCase


class ListCreateCarsViewTest(APITestCase):

    def setUp(self):
        self.c = Car.objects.create(make="123", model="1313")

    def test_a(self):
        self.assertEqual(self.c.make, "123")
