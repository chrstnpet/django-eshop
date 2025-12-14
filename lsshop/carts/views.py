from django.shortcuts import render

def cart(request):
    context = {
        'show_secondary_header': True,
    }
    return render(request, 'carts/cart.html', context)
