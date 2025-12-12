import nested_admin
from django.contrib import admin
from .models import Product, ProductColorVariant, ProductSizeVariant, Size, Color

# Nested inlines
class ProductSizeVariantInline(nested_admin.NestedTabularInline):
    model = ProductSizeVariant
    extra = 1

class ProductColorVariantInline(nested_admin.NestedTabularInline):
    model = ProductColorVariant
    inlines = [ProductSizeVariantInline]
    extra = 1

# Main Product admin
@admin.register(Product)
class ProductAdmin(nested_admin.NestedModelAdmin):
    list_display = ('product_name', 'category', 'sub_category', 'price')
    prepopulated_fields = {'slug': ('product_name',)}
    search_fields = ('product_name', 'category__category_name')
    inlines = [ProductColorVariantInline]

# Optional: separate admin pages for Size and Color if needed
@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('size',)

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('color',)
