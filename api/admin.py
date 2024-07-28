from django.contrib import admin

from api import models
# Register your models here.
admin.site.register(models.Manufacturer)
admin.site.register(models.Product)
admin.site.register(models.ProductCategory)
admin.site.register(models.Discount)