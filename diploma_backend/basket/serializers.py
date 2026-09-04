from rest_framework import serializers
from .models import BasketItem
from products.serializers import ProductSerializer


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