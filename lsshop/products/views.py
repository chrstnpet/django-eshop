from django.shortcuts import render
from .models import Product

def products(request):
    # products = Product.object.all() 
    context = {
        'show_secondary_header': True,
        'products' : 'products'
    }
    return render(request, 'products/store.html', context)