from rest_framework import serializers
from .models import Order
from reviews.models import Review


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'

    def to_representation(self, instance):
        profile = instance.full_name
        products = instance.basket.baskets.all()

        data = {
            "id": instance.pk,
            "createdAt": instance.created_at.strftime("%Y.%m.%d %H:%M"),
            "fullName": f"{profile.surname} {profile.name} {profile.patronymic}",
            "email": profile.email,
            "phone": profile.phone,
            "deliveryType": instance.delivery_type,
            "paymentType": instance.payment_type,
            "totalCost": instance.totalCost,
            "status": instance.status,
            "city": instance.city,
            "address": instance.delivery_address,
            "products": [{
                "id": item.product.pk,
                "category": item.product.category.pk,
                "price": item.product.price,
                "count": item.quantity,
                "data": item.product.date.strftime("%Y.%m.%d %H:%M"),
                "title": item.product.title,
                "description": item.product.description,
                "freeDelivery": item.product.freeDelivery,
                "images": item.product.get_images(),
                "tags": [{"id": tag.pk, "name": tag.name} for tag in item.product.tags.all()],
                "reviews": Review.objects.filter(product_id=item.product.id).count(),
                "rating": float(item.product.rating),
            } for item in products],
        }
        return data