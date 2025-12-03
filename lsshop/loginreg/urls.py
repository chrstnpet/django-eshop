from django.urls import path, include
from . import views 

app_name = 'loginreg'

urlpatterns = [
    path('login-register', views.loginreg, name='loginreg'),
]