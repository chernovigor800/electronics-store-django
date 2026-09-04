from django.contrib import admin

from .models import  Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = "pk", "created_at", "city", "delivery_address"
    list_display_links = "pk", "created_at", "city", "delivery_address"

