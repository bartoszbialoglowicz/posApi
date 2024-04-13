from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, mixins

from api import serializers
from api import models


class BaseViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin):
    permission_classes = [IsAuthenticated]


class ProductViewSet(BaseViewSet):
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all()


class ManufacturerViewSet(BaseViewSet):
    serializer_class = serializers.ManufacturerSerializer
    queryset = models.Manufacturer.objects.all()

