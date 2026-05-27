from django.contrib import admin

from .models import (
    Category,
    Product,
    ProductImage,
    Specification,
    Tag,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = "pk", "title"
    list_display_links = "pk", "title"
    ordering = ("pk", )
    search_fields = ("title", )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("pk", 'title', 'category_display', 'price', 'count')
    list_filter = ('category', 'freeDelivery')
    list_display_links = ("pk", 'title')
    search_fields = ('title', 'category__title', 'subcategory__title')
    ordering = ("pk",)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            kwargs["queryset"] = Category.objects.filter(parent__isnull=True)
        elif db_field.name == "subcategory":
            if hasattr(request, '_obj_') and request._obj_:
                parent_category = request._obj_.category
                kwargs["queryset"] = Category.objects.filter(parent=parent_category)
            else:
                kwargs["queryset"] = Category.objects.exclude(parent__isnull=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def category_display(self, obj):
        return f"{obj.category.title} → {obj.subcategory.title if obj.subcategory else ''}"
    category_display.short_description = 'Category'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = "pk", "name",
    list_display_links = "pk", "name",


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = "pk", "product", "image"
    list_display_links = "pk", "product"
    ordering = ("pk",)


@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    list_display = "pk", "name", "value"
    list_display_links = "pk", "name", "value"