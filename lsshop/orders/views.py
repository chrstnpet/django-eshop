from django.shortcuts import render, redirect
from carts.models import CartItem
from .models import Order, OrderProduct
from .forms import OrderForm
import datetime

def place_order(request):
    current_user    = request.user

    cart_items = CartItem.objects.filter(user=current_user)
    if not cart_items.exists():
        return redirect('products:products')
    
    total = sum(
        cart_item.product.color_variant.product.price * cart_item.quantity
        for cart_item in cart_items
    )
    delivery_fee = 2
    grand_total = total + delivery_fee 
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.city = form.cleaned_data['city']
            data.country = form.cleaned_data['country']
            data.postal_code = form.cleaned_data['postal_code']
            data.email = request.user.email
            data.order_total = grand_total
            data.delivery_fee = 2
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            data.order_number = (
                datetime.date.today().strftime('%Y%m%d') + str(data.id)
            )
            data.is_ordered = True
            data.save()

            for cart_item in cart_items:
                variant = cart_item.product 
                if variant.inventory < cart_item.quantity:
                    return redirect('carts:checkout')

                OrderProduct.objects.create(
                    order = data,
                    user = current_user,
                    product_variant = variant,
                    quantity = cart_item.quantity,
                    price = variant.color_variant.product.price,
                    ordered = True
                )
                variant.inventory -= cart_item.quantity
                variant.save()
            
            cart_items.delete()

            return redirect('orders:completed')
        else:
            return redirect('carts:checkout')
        
def completed(request):
    context = {
        'show_secondary_header': True,
    }
    return render(request, 'orders/completed.html', context)