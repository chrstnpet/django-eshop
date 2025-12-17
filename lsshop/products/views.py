from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ReviewRating, ProductSizeVariant, ProductColorVariant
from categories.models import Category
from django.core.paginator import Paginator
from django.db.models import Q, Avg
from collections import defaultdict
from .forms import ReviewForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from orders.models import OrderProduct

# Store main page
def products(request, category_slug=None):
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.prefetch_related('colors__sizes').all()

    products_page, paginator = paginate_queryset(request, products)
        
    product_count = products.count()

    context = {
        'products': products_page,
        'paginator': paginator,
        'product_count': product_count,
    }

    context.update(store_essentials())

    return render(request, "products/store.html", context)

def apply_filters(request):
    products = Product.objects.all()

    parent_groups = {
        "accessories": "Accessories",
        "apparel": "Apparel",
        "stationary": "Stationary",
    }

    category_filters = Q()

    for param, parent_name in parent_groups.items():
        values = request.GET.getlist(param)
        if not values:
            continue
        if "All" in values:
            category_filters |= (
                Q(category__parent__category_name=parent_name) |
                Q(category__category_name=parent_name) |
                Q(sub_category__parent__category_name=parent_name)
            )
        else:
            category_filters |= (
                Q(category__category_name__in=values) |
                Q(sub_category__category_name__in=values)
            )

    if category_filters:
        products = products.filter(category_filters)

    # Size filter
    sizes = request.GET.getlist("sizes")
    if sizes:
        products = products.filter(colors__sizes__size__size__in=sizes)

    # Availability filter
    availability = request.GET.getlist("availability")
    if "available" in availability:
        products = products.filter(colors__sizes__inventory__gt=0)
    if "unavailable" in availability:
        products = products.exclude(colors__sizes__inventory__gt=0)

    # Price filter
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")

    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    products = products.distinct()

    products_page, paginator = paginate_queryset(request, products)

    context = {
        "products": products_page,
        "paginator": paginator,
        "product_count": products.count(),
    }
    context.update(store_essentials())

    return render(request, "products/store.html", context)


# -------------------------------------------------------------------------------------
# Individual product pages
def product_detail(request, category_slug, product_slug):
    single_product = get_object_or_404(
        Product.objects.prefetch_related(
            'colors',
            'colors__sizes__size'
        ),
        category__slug=category_slug,
        slug=product_slug
    )

    color_variants = single_product.colors.all()
    sizes_by_color = defaultdict(list)

    for color in color_variants:
        for size_variant in color.sizes.all():  # include N/A
            size_name = size_variant.size.size
            if size_name == "N/A":
                size_name = "One size"
            sizes_by_color[color.id].append({
                "id": size_variant.id,
                "size": size_name,
                "inventory": size_variant.inventory,
            })

    is_product_available = any(
        size["inventory"] > 0
        for sizes in sizes_by_color.values()
        for size in sizes
    )

    orderproduct = None
    if request.user.is_authenticated:
        product_variants = ProductSizeVariant.objects.filter(color_variant__product=single_product)

        orderproduct = OrderProduct.objects.filter(
            user=request.user,
            product_variant__in=product_variants,
            ordered=True
        ).exists()

    reviews = ReviewRating.objects.filter(product_id=single_product.id)
    average_rating = reviews.aggregate(avg=Avg('rating'))['avg']

    context = {
        "single_product": single_product,
        "color_variants": color_variants,
        "sizes_by_color": dict(sizes_by_color),
        "is_product_available": is_product_available,
        "orderproduct": orderproduct,
        "reviews": reviews,
        "average_rating": average_rating,
    }

    context.update(store_essentials())

    return render(request, "products/product_detail.html", context)


#-------------------------------------------------------------------------------------
# Search
def search(request):
    keyword = request.GET.get('keyword', '').strip()[:50]
    products = Product.objects.none()

    if keyword:
        products = Product.objects.filter(
            Q(product_name__icontains=keyword) |
            Q(colors__color__color__icontains=keyword) |
            Q(category__category_name__icontains=keyword) |
            Q(colors__sizes__size__size__icontains=keyword)
        ).distinct()

    products_page, paginator = paginate_queryset(request, products)

    context = {
        'products': products_page,
        'paginator': paginator,
        'product_count': products.count(),
    }

    context.update(store_essentials())

    return render(request, 'products/store.html', context)


# -------------------------------------------------------------------------------------------
# Essentials
def store_essentials():

    accessory_categories    = ["All", "Bags", "Keychains", "Pins"]
    apparel_categories      = ["All", "Crewnecks", "Headwear", "Hoodies", "Shirts"]
    stationary_categories   = ["All", "Notebooks", "Pens", "Stickers"]
    size_categories         = ["XS", "S", "M", "L", "XL", "XXL"]
    colors                  = ["Black", "White", "Ciel", "Pink", "Mint", "Grey"]

    availability_options = [
        ("available", "Show Available Only"), 
        ("unavailable", "Show Non-Available")
    ]

    return {
        "category_groups": {
            "Accessories": {
                "items": accessory_categories
            },
            "Apparel": {
                "items": apparel_categories,
                "sizes": size_categories
            },
            "Stationary": {
                "items": stationary_categories
            },
        },
        "availability_options": availability_options,
        "colors": colors,
        "show_secondary_header": True,
    }

# -------------------------------------------------------------------------------
# Pagination
def paginate_queryset(request, queryset, per_page=9):
    paginator = Paginator(queryset, per_page)

    try:
        page = min(int(request.GET.get('page', 1)), paginator.num_pages)
    except ValueError:
        page = 1

    return paginator.page(page), paginator


# -------------------------------------------------------------------------------
@login_required(login_url='loginreg:loginreg')
def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, "Your review has been updated!")
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if not request.POST.get('rating'):
                messages.info(request, "Please add a rating.")
                return redirect(url)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id 
                data.user_id = request.user.id
                data.save()
                messages.success(request, "Thanky you! Your review has been submitted!")
                return redirect(url)
