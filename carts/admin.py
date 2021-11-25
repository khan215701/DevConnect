from django.contrib import admin
from .models import cart, cart_item

# Register your models here.

admin.site.register(cart)
admin.site.register(cart_item)
