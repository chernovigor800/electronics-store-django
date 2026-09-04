from django.db import models
from accounts.models import ProfileUser
from products.models import Product
from basket.models import Basket


class Order(models.Model):

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
    DELIVERY_OPTIONS = (
        ("delivery", "Delivery"),
        ("express", "Express delivery"),
    )
    PAYMENT_OPTIONS = (
        ("online", "Online payment"),
        ("online_any", "Online payment from a random account"),

    )

    full_name = models.ForeignKey(ProfileUser, on_delete=models.CASCADE, verbose_name="Buyer")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    products = models.ManyToManyField(Product, related_name="orders")
    city = models.CharField(max_length=100, verbose_name="Delivery city")
    delivery_address = models.TextField(max_length=200, verbose_name="Delivery address")
    delivery_type = models.CharField(max_length=20, choices=DELIVERY_OPTIONS, default="Delivery")
    payment_type = models.CharField(max_length=20, choices=PAYMENT_OPTIONS, default="Online payment")
    totalCost = models.DecimalField(
        default=0,
        max_digits=8,
        decimal_places=2,
        verbose_name="Total order amount",
    )
    status = models.CharField(max_length=255, default="inProgress")
    basket = models.ForeignKey(
        Basket, on_delete=models.CASCADE, related_name="orders", default=None
    )
    payment_error = models.CharField(max_length=255, blank=True, default="")


