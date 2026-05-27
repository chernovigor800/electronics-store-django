from rest_framework import serializers

from django.contrib.auth.models import User
from .models import ProfileUser


class UserCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    username = serializers.CharField(max_length=150, min_length=3)
    password = serializers.CharField(write_only=True, min_length=6)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Логин уже занят")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        ProfileUser.objects.create(
            user=user,
            name=validated_data['name'],
            avatar='avatar_default.jpg',
        )
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileUser
        fields = '__all__'

    def to_representation(self, instance):
        data = {
            "fullName": f"{instance.surname or ''} {instance.name or ''}".strip(),
            "email": instance.email or 'No email',
            "phone": instance.phone or '',
            "avatar": instance.get_avatar(),
        }
        return data
