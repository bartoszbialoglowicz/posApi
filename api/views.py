from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from api import serializers
from api import models

class ProductViewSet(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all()

