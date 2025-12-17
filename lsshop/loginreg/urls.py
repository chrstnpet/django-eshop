from django.urls import path, include
from . import views 

app_name = 'loginreg'

urlpatterns = [
    path('login-register/', views.loginreg, name='loginreg'),
    path('logout/', views.logout_view, name='logout'),
    path('account/', views.account, name='account'),
    path('my_orders/', views.my_orders, name='my_orders'),
]