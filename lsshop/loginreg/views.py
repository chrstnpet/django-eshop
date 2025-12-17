from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login , logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.cache import cache
import requests
from orders.models import Order
from products.models import Product, Wishlist

# ---------------------------------------------------------------------------------------------
# Helper function to get client IP address
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# ---------------------------------------------------------------------------------------------
# Login and Register
MAX_ATTEMPTS_LOGIN      = 5
MAX_ATTEMPTS_REGISTER   = 3 
BLOCK_TIME_LOGIN        = 300
BLOCK_TIME_REGISTER     = 9000

def loginreg(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect('home:home')

    if request.method == "POST" and 'login_submit' in request.POST:
        login_ip        = get_client_ip(request)
        login_key       = f"login_attempts_{login_ip}"
        attempts_login  = cache.get(login_key, 0)

        if request.user.is_authenticated:
            messages.info(request, "You are already logged in. Please logout first to login with another account.", extra_tags="loginfail")
            return redirect('loginreg:loginreg')

        if attempts_login >= MAX_ATTEMPTS_LOGIN:
            messages.error(request, "Too many login attempts. Please try again later.", extra_tags="loginfail")
            return redirect('loginreg:loginreg')

        username    = request.POST.get('username')
        password    = request.POST.get('password')
        user        = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            cache.delete(login_key) 
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                return redirect(nextPage)
            except:
                return redirect('home:home')
        else:
            attempts_login += 1
            cache.set(login_key, attempts_login, BLOCK_TIME_LOGIN)
            if attempts_login < MAX_ATTEMPTS_LOGIN:
                messages.error(request, "Invalid username or password", extra_tags="loginfail")
            else:
                messages.error(request, "Too many login attempts. Please try again later.", extra_tags="loginfail")
            return redirect('loginreg:loginreg')


    # Register
    elif 'register_submit' in request.POST:
        register_ip         = get_client_ip(request)
        register_key        = f"register_attempts_{register_ip}"
        attempts_register   = cache.get(register_key, 0)

        if request.user.is_authenticated:
            messages.info(request, "You can't register a new user while you're logged in. Please log out first.", extra_tags="registrationfail")
            return redirect('loginreg:loginreg')
        
        if attempts_register >= MAX_ATTEMPTS_REGISTER:
            messages.error(request, "Too many registration attempts. Please try again later.", extra_tags="registrationfail")
            return redirect('loginreg:loginreg')

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match", extra_tags="registration")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken", extra_tags="registration")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered", extra_tags="registration")
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            user.save()
            login(request, user)
            messages.success(
                request, 
                "Account created successfully! Have fun shopping! 🎉", 
                extra_tags="regsuccess"
            )
            attempts_register +=1
            cache.set(register_key, attempts_register, BLOCK_TIME_REGISTER)
            return redirect('home:home')

    return render(request, 'loginreg/loginreg.html', {'loginreg': loginreg})


# ---------------------------------------------------------------------------------------------
# Logout 
def logout_view(request):
    logout(request)
    return redirect('loginreg:loginreg')


# ---------------------------------------------------------------------------------------------
# Account Management

MAX_ATTEMPTS_INFO_CHANGE        = 2
MAX_ATTEMPTS_PASSWORD_CHANGE    = 1
BLOCK_TIME_CHANGE               = 86400

@login_required
def account(request):
    user = request.user
    open_section = None

    account_ip              = get_client_ip(request)
    info_key                = f"change_info_{account_ip}"
    pass_key                = f"change_pass_{account_ip}"
    attempts_change_info    = cache.get(info_key, 0)
    attempts_change_pass    = cache.get(pass_key, 0)

    if request.method == "POST":

        # Account info update
        if 'update_account' in request.POST:
            username = request.POST.get('username')
            email = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')

            if User.objects.exclude(pk=user.pk).filter(username=username).exists():
                messages.error(request, "Username is already taken", extra_tags="changeerror")
            elif User.objects.exclude(pk=user.pk).filter(email=email).exists():
                messages.error(request, "Email already registered", extra_tags="changeerror")
            else:
                attempts_change_info +=1
                cache.set(info_key, attempts_change_info, BLOCK_TIME_CHANGE)
                if attempts_change_info <= MAX_ATTEMPTS_INFO_CHANGE:
                    messages.success(request, "Account updated successfully!", extra_tags="changesuccess")
                    user.username = username
                    user.email = email
                    user.first_name = first_name
                    user.last_name = last_name
                    user.save()
                else:
                    messages.info(request, "You can only change your information twice per day. Please revisit tomorrow.", extra_tags="changefail")

            open_section = 'accountDetails'  # Keep Account Info open

        # Password update
        elif 'update_password' in request.POST:
            password = request.POST.get('password')
            password_check = request.POST.get('passwordCheck')

            if password != password_check:
                messages.error(request, "Passwords do not match", extra_tags="changeerror")
            elif not password:
                messages.error(request, "Password cannot be empty", extra_tags="changeerror")
            else:
                attempts_change_pass +=1 
                cache.set(pass_key, attempts_change_pass, BLOCK_TIME_CHANGE)
                if attempts_change_pass <= MAX_ATTEMPTS_PASSWORD_CHANGE:
                    user.set_password(password)
                    user.save()
                    messages.success(request, "Password updated successfully!", extra_tags="changesuccess")
                    update_session_auth_hash(request, user)
                else:
                    messages.info(request, "You can only change your password once per day. Please revisit tomorrow.", extra_tags="changefail")

            open_section = 'changePassword'

    information = [
        ("username", user.username),
        ("email", user.email),
        ("first_name", user.first_name),
        ("last_name", user.last_name),
    ]

    accordion_sections = [
        {
            "id": "accountDetails",
            "heading": "Account Info",
            "button_name": "update_account",
        },
        {
            "id": "changePassword",
            "heading": "Password Reset",
            "button_name": "update_password",
        },
        {
            "id": "orderHistory",
            "heading": "Order History",
        },
        {
            "id": "viewWishlist",
            "heading": "Wishlist",
        }
    ]

    orders = Order.objects.order_by('created_at').filter(user_id=request.user.id, is_ordered=True)
    orders_count = orders.count()

    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')

    context = {
        'user': user,
        'open_section': open_section,
        'information': information,
        'accordion_sections': accordion_sections,
        'show_secondary_header': True,
        'orders_count': orders_count,
        'orders': orders,
        'wishlist_items': wishlist_items,
    }

    return render(request, 'loginreg/account.html', context)

@login_required(login_url='loginreg:loginreg')
def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    context = {
        "orders": orders,
    }

    return render(request, 'account/my_orders.html', context)

@login_required
def wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    wishlist_item = Wishlist.objects.filter(
        user=request.user,
        product=product
    ).first()

    if wishlist_item:
        wishlist_item.delete()
    else:
        Wishlist.objects.create(
            user=request.user,
            product=product
        )

    return redirect(request.META.get('HTTP_REFERER', '/'))
