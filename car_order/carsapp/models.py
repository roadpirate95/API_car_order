import datetime
from django.utils import timezone
from django.db import models


class CarMake(models.Model):

    title = models.CharField(max_length=250)

    def __str__(self):
        return self.title


class CarModel(models.Model):

    title = models.CharField(max_length=250)
    car_make_id = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name='car_models')

    def __str__(self):
        return self.title


class Color(models.Model):

    title = models.CharField(max_length=250)

    def __str__(self):
        return self.title


class Order(models.Model):

    color_id = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='order_color')
    car_model_id = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name='order_model')
    date = models.DateField(default=datetime.date.today)
    amount = models.PositiveIntegerField()

