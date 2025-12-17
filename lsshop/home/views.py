from django.shortcuts import render
from orders.models import OrderProduct
from products.models import Product
from django.db.models import Sum

# Bringing to the home page the 4 most bought items if there are more than 4 distinct items that have been bought, else I have my default ones that I want to promote
def home(request):
    popular_products_qs = (
        OrderProduct.objects
        .filter(ordered=True)
        .values('product_variant__color_variant__product')
        .annotate(total_sold=Sum('quantity'))
        .order_by('-total_sold')[:4]
    )

    if popular_products_qs.count() >= 4:
        product_ids = [
            item['product_variant__color_variant__product']
            for item in popular_products_qs
        ]
        popular_products = Product.objects.filter(id__in=product_ids)
    else:
        popular_products = None

    return render(request, 'home/home.html', {'popular_products': popular_products})
