from django.contrib import admin
from .models import *

# Register your models here.
class adminOrder(admin.ModelAdmin):
    list_display = ['user','is_ordered','shipping_address']

class adminOrderItem(admin.ModelAdmin):
    list_display = ['product','quantity','order']

class adminShippingAddress(admin.ModelAdmin):
    list_display = ['user','country','city','street_address','house_address']




admin.site.register(Order,adminOrder)
admin.site.register(OrderItem,adminOrderItem)
admin.site.register(Product)
admin.site.register(ShippingAddress,adminShippingAddress)