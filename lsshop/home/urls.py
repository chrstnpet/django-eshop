from django.urls import path, include
from django.contrib import admin
from . import views 

app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),
]