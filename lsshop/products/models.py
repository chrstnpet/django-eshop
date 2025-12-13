from django.db import models
from categories.models import Category
from django.urls import reverse
from django.core.exceptions import ValidationError

def validate_image(image):
    if image.size > 2 * 1024 * 1024:
        raise ValidationError("Image file too large")

class Size(models.Model):
    size = models.CharField(max_length=4)

    def __str__(self):
        return self.size


class Color(models.Model):
    color = models.CharField(max_length=30)

    def __str__(self):
        return self.color


class Product(models.Model):
    product_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='subcategory',
        null=True,
        blank=True
    )

    price = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    description = models.TextField(max_length=500, blank=True)

    def get_url(self):
        return reverse('products:product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name


class ProductColorVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="colors")
    color = models.ForeignKey(Color, on_delete=models.CASCADE)

    front_image = models.ImageField(upload_to='products/', blank=True, null=True, validators=[validate_image])
    back_image = models.ImageField(upload_to='products/', blank=True, null=True, validators=[validate_image])

    def is_available(self):
        return self.sizes.filter(inventory__gt=0).exists()

    def __str__(self):
        return f"{self.product.product_name} - {self.color}"

    class Meta:
        unique_together = ('product', 'color')

class ProductSizeVariant(models.Model):
    color_variant = models.ForeignKey(
        ProductColorVariant,
        on_delete=models.CASCADE,
        related_name="sizes"
    )

    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    inventory = models.PositiveIntegerField(default=0)

    def is_available(self):
        return self.inventory > 0

    def __str__(self):
        return f"{self.color_variant} - {self.size}"

    class Meta:
        unique_together = ('color_variant', 'size')
