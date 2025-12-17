from django.urls import path, include
from . import views

app_name = 'products'

urlpatterns = [
    path('products/', views.products, name='products'),
    path('products/category/<slug:category_slug>/', views.products, name='products_by_category'),
    path('products/category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path("apply-filters/", views.apply_filters, name='apply_filters'),
    path('products/search/', views.search, name='search'),
    path('cart/', include('carts.urls',)),
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review')
]