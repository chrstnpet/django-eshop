from django.shortcuts import render, get_object_or_404
from .models import Product, ProductSizeVariant, ProductColorVariant, Size, Color
from categories.models import Category
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def products(request, category_slug=None):
    categories  = None 
    products    = None 

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.prefetch_related('colors__sizes').all()

    page = request.GET.get('page', 1)
    paginator = Paginator(products, 9)
    try:
        products_page = paginator.page(page)
    except PageNotAnInteger:
        products_page = paginator.page(1)
    except EmptyPage:
        products_page = paginator.page(paginator.num_pages)
        
    product_count = products.count()

    accessory_categories    = ["All", "Bags", "Keychains", "Pins"]
    apparel_categories      = ["All", "Crewnecks", "Headwear", "Hoodies", "Shirts"]
    stationery_categories   = ["All", "Notebooks", "Pens", "Stickers"]
    size_categories         = ["All", "XS", "S", "M", "L", "XL", "XXL"]
    color_categories        = ["All", "Black", "White", "Ciel", "Pink", "Mint", "Grey"]
    availability_options    = [
        ("available", "Show Available Only"), 
        ("unavailable", "Show Non-Available")
    ]

    context = {
        'products': products_page,
        'paginator': paginator,
        'product_count': product_count,
        'categories': categories,
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
        'show_secondary_header': True,
    }

    return render(request, "products/store.html", context)

def product_detail(request, category_slug, product_slug):
    single_product = get_object_or_404(
        Product.objects.prefetch_related('colors__sizes__size'),
        category__slug=category_slug,
        slug=product_slug
    )

    color_variants = single_product.colors.all()

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
    }

    return render(request, 'products/product_detail.html', context)