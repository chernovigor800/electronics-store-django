from django.db import models
from django.contrib.auth.models import User


class Basket(models.Model):
    DoesNotExist = "Busket does not exist"
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Basket of {self.user.username if self.user else 'anonymous'}"


class BasketItem(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name="baskets")
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name="products")
    quantity = models.PositiveIntegerField(default=0)