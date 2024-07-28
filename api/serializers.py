from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from api import models


class ManufacturerSerializer(ModelSerializer):
    class Meta:
        model = models.Manufacturer
        fields = ('id','name', 'country')


class CategorySerializer(ModelSerializer):
    class Meta:
        model = models.ProductCategory
        fields = ('id', 'name', 'description')

class ProductSerializer(ModelSerializer):
    manufacturer = ManufacturerSerializer(many=False, read_only=True)
    manufacturer_id = serializers.PrimaryKeyRelatedField(
        queryset=models.Manufacturer.objects.all(),
        source='manufacturer',
        write_only=True,
        required=False
    )
    category = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model =  models.Product
        fields = ('id', 'name', 'price', 'manufacturer', 'manufacturer_id', 
                  'category', 'stock_quantity', 'barcode', 'image', 'is_active',
                  'created_at', 'updated_at')

    def create(self, validated_data):
        manufacturer_id = validated_data.pop('manufacturer_id', None)
        if manufacturer_id is not None:
            validated_data['manufacturer'] = models.Manufacturer.objects.get(pk=manufacturer_id)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        manufacturer_id = validated_data.pop('manufacturer_id', None)
        if manufacturer_id is not None:
            instance.manufacturer = models.Manufacturer.objects.get(pk=manufacturer_id)
        return super().update(instance, validated_data)


class DiscountSerializer(ModelSerializer):
    product = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = models.Discount
        fields = (
            'id', 'product', 'discount_percentage', 'start_date', 'end_date'
        )