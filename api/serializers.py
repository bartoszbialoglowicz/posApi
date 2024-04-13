from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from api import models


class ManufacturerSerializer(ModelSerializer):
    class Meta:
        model = models.Manufacturer
        fields = ('id','name', 'country')


class ProductSerializer(ModelSerializer):
    manufacturer = ManufacturerSerializer(many=False, read_only=True)
    class Meta:
        model =  models.Product
        fields = ('id', 'name', 'price', 'manufacturer')