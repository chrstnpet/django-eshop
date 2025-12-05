from django.contrib import admin
from .models import Product, Size, Color

class ProductAdmin(admin.ModelAdmin):
    list_display        = ('product_name', 'category', 'sub_category', 'size', 'color', 'is_available', 'inventory', 'price')
    list_filter         = ('category', 'sub_category', 'size', 'color', 'is_available')
    search_fields       = ('product_name')
    prepopulated_fields = {'slug': ('product_name',)}

class SizeAdmin(admin.ModelAdmin):
    list_display        = ('size',)

class ColorAdmin(admin.ModelAdmin):
    list_display        = ('color',)

admin.site.register(Product)