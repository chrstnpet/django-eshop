from django.urls import path 
from . import views

app_name = 'products'

urlpatterns = [
    path('products/', views.products, name='products'),
    path('products/category/<slug:category_slug>/', views.products, name='products_by_category'),
    path('products/category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('products/search/', views.search, name='search'),
]