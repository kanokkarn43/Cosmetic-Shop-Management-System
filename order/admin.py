from django.contrib import admin

# Create Order models

from .models import Order 
from .models import Member

admin.site.register(Order)
admin.site.register(Member)

