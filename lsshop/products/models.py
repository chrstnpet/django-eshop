from django.db import models
from categories.models import Category

class Product(models.Model):
    product_name            = models.CharField(max_length=50)
    category        = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category    = models.CharField(max_length=50, blank=True) # will have to change this to foreign key once i add the subcategories
    color           = models.CharField(max_length=30, blank=True)
    is_available    = models.BooleanField(default=True)
    inventory       = models.IntegerField(default=1)
    size            = models.CharField(max_length=10)
    price           = models.DecimalField(max_digits=8, decimal_places=2)
    product_image   = models.ImageField(upload_to='products/', blank=True, null=True)
    description     = models.TextField(max_length=500, blank=True)


    def __str__(self):
        return self.product_name
