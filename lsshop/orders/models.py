from django.db import models
from django.contrib.auth.models import User
from products.models import ProductSizeVariant
    
class Order(models.Model):
    status = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    user            = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order_number    = models.CharField(max_length=20)
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    phone           = models.CharField(max_length=15)
    email           = models.EmailField(max_length=50)
    address_line_1  = models.CharField(max_length=50)
    address_line_2  = models.CharField(max_length=50, blank=True)
    country         = models.CharField(max_length=50)
    city            = models.CharField(max_length=50)
    postal_code     = models.CharField(max_length=10, blank=True, null=True)
    order_total     = models.FloatField()
    delivery_fee    = models.IntegerField(default=2)
    status          = models.CharField(max_length=10, choices=status, default='New')
    ip              = models.CharField(blank=True, max_length=20)
    is_ordered      = models.BooleanField(default=False)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_number
    
class OrderProduct(models.Model):
    order           = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    product_variant = models.ForeignKey(ProductSizeVariant, on_delete=models.PROTECT)
    quantity        = models.PositiveBigIntegerField()
    price           = models.FloatField()
    ordered         = models.BooleanField(default=False)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product_variant}"