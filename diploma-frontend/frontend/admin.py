from django.contrib import admin
from .models import Category, Product, BasketItem, CustomerOrder, OrderItem
# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(BasketItem)
admin.site.register(CustomerOrder)
admin.site.register(OrderItem)