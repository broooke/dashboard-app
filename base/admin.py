from django.contrib import admin
from .models import Customer, Tag, Order, Product, Profile

# Register your models here.

admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(Tag)
admin.site.register(Profile)