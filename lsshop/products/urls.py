from django.urls import path 
from . import views

app_name = 'products'

urlpatterns = [
    path('products/', views.products, name='products'),
    path('products/<slug:category_slug>/', views.products, name='products_by_category'),
]