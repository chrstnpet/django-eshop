from django.shortcuts import render, get_object_or_404
from .models import Product, ProductSizeVariant, ProductColorVariant, Size, Color
from categories.models import Category
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

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


# -------------------------------------------------------------------------------------
# Individual product pages
def product_detail(request, category_slug, product_slug):
    single_product = get_object_or_404(
        Product.objects.prefetch_related('colors__sizes__size'),
        category__slug=category_slug,
        slug=product_slug
    )

    color_variants = single_product.colors.all()

    is_product_available = color_variants.filter(
        sizes__inventory__gt=0
    ).exists()

    selected_variant_id = request.GET.get('color')

    if selected_variant_id:
        selected_variant = color_variants.filter(id=selected_variant_id).first()
    else:
        selected_variant = color_variants.first()

    if selected_variant:
        size_variants = selected_variant.sizes.all().select_related('size')
        size_variants = size_variants.exclude(size__size="N/A")
        if not size_variants.exists():
            size_variants = None
    else:
        size_variants = None


    context = {
        'single_product': single_product,
        'color_variants': color_variants,
        'selected_variant': selected_variant,
        'size_variants': size_variants,
        'is_product_available': is_product_available,
    }

    context.update(store_essentials())

    return render(request, 'products/product_detail.html', context)


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
    stationery_categories   = ["All", "Notebooks", "Pens", "Stickers"]
    size_categories         = ["All", "XS", "S", "M", "L", "XL", "XXL"]
    color_categories        = ["All", "Black", "White", "Ciel", "Pink", "Mint", "Grey"]
    availability_options    = [
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
            "Stationery": {
                "items": stationery_categories
            },
        },
        "availability_options": availability_options,
        "colors": color_categories,
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
