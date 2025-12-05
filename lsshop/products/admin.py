from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'category', 'is_available', 'inventory', 'price')
    prepopulated_fields = {'slug': ('product_name',)}

admin.site.register(Product)