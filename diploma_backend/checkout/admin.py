from django.contrib import admin

from .models import Sale, DeliveryPrice, Payment


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = "pk", "product", "date_from", "date_to", "discount"
    list_display_links = "pk", "product", "date_from", "date_to", "discount"


@admin.register(DeliveryPrice)
class DeliveryPriceAdmin(admin.ModelAdmin):
    list_display = "pk", "delivery_cost", "delivery_express_cost", "delivery_free_minimum_cost"
    list_display_links = "pk", "delivery_cost", "delivery_express_cost", "delivery_free_minimum_cost"


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = "pk", "order", "card_number", "success"
    list_display_links = "pk", "order", "card_number"
