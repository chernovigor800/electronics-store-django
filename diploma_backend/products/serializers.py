from django.db.models import Count, Avg, Min
from rest_framework import serializers

from .models import (
    Product,
    Tag,
    ProductImage,
    Specification,
)
from basket.models import BasketItem
from reviews.models import Review


class BannerCategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    description = serializers.CharField(default="Feature category")
    price = serializers.FloatField(default=0)
    count = serializers.IntegerField(default=999)
    date = serializers.CharField(default="2026.01.18 11:00")
    freeDelivery = serializers.BooleanField(default=False)
    category = serializers.IntegerField()
    images = serializers.ListField()
    tags = serializers.ListField()
    reviews = serializers.IntegerField(default=0)
    rating = serializers.FloatField(default=0)


    def to_representation(self, instance):
        min_price = Product.objects.filter(category=instance).aggregate(
            min_price=Min('price')
        )['min_price'] or 0

        return {
            'id': instance.id,
            'title': instance.title,
            'description': "Featured banner category",
            'price': float(min_price),
            'count': 999,
            'freeDelivery': False,
            'category': instance.id,
            'images': [instance.get_image()] if instance.get_image() else [],
            'tags': [{"id": 1, "name": "banner"}],
            'date': "2026.01.18 11:00",
            'reviews': 0,
            'rating': 0,
        }


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'count', 'date',
                  'freeDelivery', 'category', 'images', 'tags', 'reviews', 'rating']

    def to_representation(self, instance):
        data = {
            'id': instance.pk,
            'title': instance.title,
            'description': instance.description,
            'price': float(instance.price),
            'count': instance.count,
            'freeDelivery': instance.freeDelivery,
            'category': instance.category.pk if instance.category else None,
        }
        data['images'] = instance.get_images() if hasattr(instance, 'get_images') else []
        data['tags'] = [{"id": tag.pk, "name": tag.name} for tag in instance.tags.all()]

        if instance.date:
            data['date'] = instance.date.strftime("%Y.%m.%d %H:%M")

        reviews = Review.objects.filter(product_id=instance.id).aggregate(
            count=Count('id'), avg=Avg('rate')
        )
        data['reviews'] = reviews['count'] or 0
        data['rating'] = reviews['avg'] or 0 if reviews['count'] else "No reviews yet"

        return data


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = ('image',)


class ProductSpecificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Specification
        fields = ('name', 'value')


class TagListSerializer(serializers.ModelSerializer):

    id = serializers.CharField(source="name")

    class Meta:
        model = Tag
        fields = ["id", "name"]


class DetailsSerializer(ProductSerializer):
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        specifications = Specification.objects.filter(pk=instance.id)
        reviews = Review.objects.filter(product_id=instance.id).order_by('date')

        rep['specifications'] = [{'name': spec.name, 'value': spec.value} for spec in specifications]
        rep['reviews'] = [
            {
                'author': review.review_author_name or f'{review.author.name or ""} {review.author.surname or ""}'.strip() or "No name",
                'email': review.review_author_email or review.author.email or "",
                'text': review.text or "",
                'rate': review.rate,
                'date': review.date.strftime("%Y.%m.%d %H:%M") if review.date else "",
            }
            for review in reviews
        ]

        return rep


class BasketItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = BasketItem
        fields = (
            "product", "count",
        )

    def to_representation(self, instance):
        data = ProductSerializer(instance.product).data
        data['count'] = instance.quantity

        return data