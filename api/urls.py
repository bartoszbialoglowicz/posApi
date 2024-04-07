from django.urls import path

from api import views

app_name = 'api'

urlpatterns = [
    path('products', views.ProductViewSet.as_view(), name='products'),
]
