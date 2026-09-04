from rest_framework import serializers
from reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

    def to_representation(self, instance):
        profile = instance.author

        data = {
            "id": instance.pk,
            "text": instance.text,
            "rate": instance.rate,
            "createdAt": instance.created_at.strftime("%Y.%m.%d %H:%M") if instance.created_at else None,
            "fullName": f"{profile.surname} {profile.name} {profile.patronymic}".strip(),
            "email": profile.email,
            "productId": instance.product.pk,
            "productTitle": instance.product.title,
        }
        return data