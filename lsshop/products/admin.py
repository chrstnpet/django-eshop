import nested_admin
from django.contrib import admin
from .models import Product, ProductColorVariant, ProductSizeVariant, Size, Color, ReviewRating

class ProductSizeVariantInline(nested_admin.NestedTabularInline):
    model = ProductSizeVariant
    extra = 1

class ProductColorVariantInline(nested_admin.NestedTabularInline):
    model = ProductColorVariant
    inlines = [ProductSizeVariantInline]
    extra = 1

@admin.register(Product)
class ProductAdmin(nested_admin.NestedModelAdmin):
    list_display = ('product_name', 'category', 'sub_category', 'price')
    prepopulated_fields = {'slug': ('product_name',)}
    search_fields = ('product_name', 'category__category_name')
    inlines = [ProductColorVariantInline]

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('size',)

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('color',)

admin.site.register(ReviewRating)
