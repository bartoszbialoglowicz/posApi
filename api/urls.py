from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('manufacturers', views.ManufacturerViewSet)
router.register('categories', views.CategoryViewSet)
router.register('discounts', views.DiscountViewSet)

app_name = 'api'

urlpatterns = [
    path('', include(router.urls))
]
