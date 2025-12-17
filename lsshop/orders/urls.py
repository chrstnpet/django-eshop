from django.urls import path 
from . import views 

app_name = 'orders'

urlpatterns = [
    path('orders/place_order/', views.place_order, name='place_order'),
    path('orders/completed', views.completed, name='completed'),
]