from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


def avatar_image_directory_path(instance, filename):
    return f"profiles/profile_{instance.pk}/avatar/{filename}"


class ProfileUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name="Name", blank=True, null=True)
    surname = models.CharField(max_length=255, verbose_name="Surname", blank=True, null=True)
    patronymic = models.CharField(max_length=255, verbose_name="Patronymic", blank=True, null=True)
    phone = models.CharField(max_length=15, verbose_name="Phone number", blank=True, null=True)
    email = models.EmailField(max_length=200, verbose_name="Email", blank=True, null=True)
    avatar = models.ImageField(null=True, blank=True, upload_to=avatar_image_directory_path)

    def get_avatar(self):
        if self.avatar:
            return {
                "src": self.avatar.url,
                "alt": f"{self.surname or self.name or 'User'} avatar",
            }
        return {
            "src": "/media/avatar_default.jpg",
            "alt": "Default avatar",
        }

    def __str__(self):
        if self.name:
            return self.name
        if self.surname:
            return self.surname
        try:
            return self.user.username
        except:
            return "No name user"
