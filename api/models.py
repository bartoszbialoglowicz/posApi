from django.db import models


class Manufacturer(models.Model):
    name = models.CharField(max_length=128, unique=True)
    country = models.CharField(max_length=80)


class Product(models.Model):
    name = models.CharField(max_length=128, unique=True)
    price = models.IntegerField()
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
