from django.contrib import admin
from .models import Order, ShipLines, OrderDetail

admin.site.register(Order)
admin.site.register(ShipLines)
admin.site.register(OrderDetail)