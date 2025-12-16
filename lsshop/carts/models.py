from django.db import models
from products.models import ProductSizeVariant

class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Cart({self.user or self.cart_id})"


class CartItem(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(ProductSizeVariant, on_delete=models.CASCADE, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.color_variant.product.price * self.quantity

    def __str__(self):
        return str(self.product)

