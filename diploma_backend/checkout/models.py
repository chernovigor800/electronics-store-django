from django.db import models
from products.models import Product
from orders.models import Order


class Sale(models.Model):

    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='sale_info')
    date_from = models.DateField()
    date_to = models.DateField()
    discount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Sale #{self.pk}"


class DeliveryPrice(models.Model):

    class Meta:
        verbose_name = "Delivery cost"

    delivery_cost = models.DecimalField(
        default=0,
        max_digits=8,
        decimal_places=2,
        verbose_name="Delivery cost",
    )

    delivery_express_cost = models.DecimalField(
        default=0,
        max_digits=8,
        decimal_places=2,
        verbose_name="Express delivery cost",
    )

    delivery_free_minimum_cost = models.DecimalField(
        default=0,
        max_digits=8,
        decimal_places=2,
        verbose_name="Minimum order amount for free shipping",
    )


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="pay_order")
    card_number = models.CharField(max_length=16)
    validity_period = models.CharField(max_length=20)
    success = models.BooleanField(default=False)
