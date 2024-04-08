from rest_framework.serializers import ModelSerializer

from api import models

class ProductSerializer(ModelSerializer):
    class Meta:
        model =  models.Product
        fields = ('name', 'price')


class ManufacturerSerializer(ModelSerializer):
    class Meta:
        model = models.Manufacturer
        fields = ('name', 'country')