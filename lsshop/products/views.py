from django.shortcuts import render, get_object_or_404
from .models import Product, ProductSizeVariant, ProductColorVariant, Size, Color
from categories.models import Category

def products(request, category_slug=None):
    categories  = None 
    products    = None 

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.prefetch_related('colors__sizes').all()
        
    product_count = products.count()

    accessory_categories    = ["All", "Bags", "Keychains", "Pins"]
    apparel_categories      = ["All", "Crewnecks", "Headwear", "Hoodies", "Shirts"]
    stationery_categories   = ["All", "Notebooks", "Pens", "Stickers"]
    size_categories         = ["All", "XS", "S", "M", "L", "XL", "XXL"]
    availability_options    = [
        ("available", "Show Available Only"), 
        ("unavailable", "Show Non-Available")
    ]

    context = {
        'products': products,
        'product_count': product_count,
        "category_groups": {
            "Accessories": {
                "items": accessory_categories
            },
            "Apparel": {
                "items": apparel_categories,
                "sizes": size_categories
            },
            "Stationery": {
                "items": stationery_categories
            }
        },
        "availability_options": availability_options,
        'show_secondary_header': True,
    }

    return render(request, "products/store.html", context)