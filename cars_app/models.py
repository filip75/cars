from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Car(models.Model):
    make = models.CharField(null=False, max_length=100, blank=False)
    model = models.CharField(null=False, max_length=100, blank=False)
    
    # class Meta:
    #     unique_together = [["make", "model"]]


class CarRate(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="rates")
    value = models.IntegerField(null=False, validators=[MinValueValidator(1), MaxValueValidator(5)])