from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem
from products.models import ProductSizeVariant
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# ---------------------------------------------------------------
def get_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key

        cart, created = Cart.objects.get_or_create(session_key=session_key)

    return cart


@login_required(login_url='loginreg:loginreg')
def add_cart(request, product_id):
    product = get_object_or_404(ProductSizeVariant, id=product_id)
    cart = get_cart(request)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        user=request.user,
        defaults={"quantity": 1}
    )

    if not created:
        if cart_item.quantity >= product.inventory:
            messages.info(request, "Maximum available stock reached.")
        else:
            cart_item.quantity += 1
            cart_item.save()

    return redirect('carts:cart')


# ---------------------------------------------------------------
@login_required(login_url='loginreg:loginreg')
def remove_cart(request, product_id):
    cart = cart = get_cart(request)
    product = get_object_or_404(ProductSizeVariant, id=product_id)
    cart_item = get_object_or_404(CartItem, product=product, cart=cart, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('carts:cart')

@login_required(login_url='loginreg:loginreg')
def remove_cart_item(request, product_id):
    cart = cart = get_cart(request)
    product = get_object_or_404(ProductSizeVariant, id=product_id)
    cart_item = get_object_or_404(CartItem, product=product, cart=cart, user=request.user)
    cart_item.delete()

    return redirect('carts:cart')

# ---------------------------------------------------------------
@login_required(login_url='loginreg:loginreg')
def cart(request, total=0, quantity=0, cart_items=None):
    grand_total = 0
    delivery_tax = 2
    try:
        cart = cart = get_cart(request)
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.color_variant.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        grand_total = total + delivery_tax
    except Cart.DoesNotExist:
        cart_items = []
        total = 0
        quantity = 0
        pass
    context = {
        'total': total,
        'delivery_tax': delivery_tax,
        'grand_total': grand_total,
        'quantity': quantity,
        'cart_items': cart_items,
        'show_secondary_header': True,
    }
    return render(request, 'carts/cart.html', context)

# ---------------------------------------------------------------
@login_required(login_url='loginreg:loginreg')
def checkout(request, total=0, quantity=0):
    user = request.user
    billing = [
        ("first_name", user.first_name),
        ("last_name", user.last_name),
        ("Address Line 1", ""),
        ("Address Line 2", ""),
        ("City", ""),
        ("Postal Code", ""),
        ("Country", ""),
        ("Phone Number", ""),
    ]

    grand_total = 0
    delivery_tax = 2
    try:
        cart = cart = get_cart(request)
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.color_variant.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        grand_total = total + delivery_tax
    except Cart.DoesNotExist:
        cart_items = []
        total = 0
        quantity = 0
        pass

    context = {
        'total': total,
        'delivery_tax': delivery_tax,
        'grand_total': grand_total,
        'quantity': quantity,
        'cart_items': cart_items,
        'billing': billing,
        'show_secondary_header': True,
    }

    return render(request, 'carts/checkout.html', context)