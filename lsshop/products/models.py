from django.db import models
from categories.models import Category

class Size(models.Model):
    size                    = models.CharField(max_length=4)

    def __str__(self):
        return self.size
    
class Color(models.Model):
    color                   = models.CharField(max_length=30)

    def __str__(self):
        return self.color

class Product(models.Model):
    product_name            = models.CharField(max_length=50)
    slug                    = models.SlugField(max_length=200, unique=True, blank=True)
    
    category                = models.ForeignKey(
        Category, 
        on_delete           = models.CASCADE,
        limit_choices_to    = {'parent_isnull': True}
    )
    sub_category = models.ForeignKey(
        Category,
        on_delete           = models.SET_NULL,
        related_name        = 'subcategory',
        limit_choices_to    = {'parent_isnull': False}, 
        null                = True,
        blank               = True
    )
    
    color                   = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True)
    size                    = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, blank=True)

    is_available            = models.BooleanField(default=True)
    inventory               = models.IntegerField(default=1)
    price                   = models.DecimalField(max_digits=8, decimal_places=2)
    product_image           = models.ImageField(upload_to='products/', blank=True, null=True)
    description             = models.TextField(max_length=500, blank=True)


    def __str__(self):
        return self.product_name
