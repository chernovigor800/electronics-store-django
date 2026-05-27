from django.contrib import admin

from .models import BasketItem, Basket


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = "pk", "user", "created_at"
    list_display_links = "pk", "user", "created_at"


@admin.register(BasketItem)
class BasketItemAdmin(admin.ModelAdmin):
    list_display = "pk", "product", "basket", "quantity"
    list_display_links = "pk", "product", "basket", "quantity"

