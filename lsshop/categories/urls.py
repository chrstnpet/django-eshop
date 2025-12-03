from django.urls import path, include
from . import views 

app_name = 'categories'

urlpatterns = [
    path('categories', views.categories, name='categories'),
]