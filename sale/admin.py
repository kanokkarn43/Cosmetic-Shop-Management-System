from django.contrib import admin

# Register your models here.

# Create models
from .models import AllProduct
from .models import Member
from .models import Order
from .models import OrderLineItem

admin.site.register(AllProduct)
admin.site.register(Member)
admin.site.register(Order)
admin.site.register(OrderLineItem)
