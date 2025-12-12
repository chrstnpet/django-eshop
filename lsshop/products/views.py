from django.shortcuts import render
from .models import Product, ProductSizeVariant, ProductColorVariant, Size, Color

def products(request):
    products = Product.objects.prefetch_related(
        'colors__sizes'
    ).all()
    
    sizes = Size.objects.all()
    categories = Product.objects.values_list('category', flat=True).distinct()

    context = {
        'products': products,
        'sizes': sizes,
        'categories': categories,
    }
    return render(request, 'products/store.html', context)