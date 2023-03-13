from django.contrib import admin
from .models import Product, ProductGroup, ProductModel

admin.site.register(Product)
admin.site.register(ProductGroup)
admin.site.register(ProductModel)
