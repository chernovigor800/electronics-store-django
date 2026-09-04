from django.contrib import admin

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = "pk", "author", "rate", "date", "product"
    list_display_links = "pk", "author", "rate", "date", "product"