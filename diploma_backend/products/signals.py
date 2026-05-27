import os
import shutil
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.conf import settings
from .models import Product, Category


@receiver(pre_delete, sender=Category)
def delete_category_image_folder(sender, instance, **kwargs):
    slug = (
        instance.title.lower().replace(" ", "_").replace("/", "_").replace("-", "_"))
    category_folder_path = os.path.join(
        settings.MEDIA_ROOT,"categories",f"{instance.pk}_{slug}")

    if os.path.isdir(category_folder_path):
        try:
            shutil.rmtree(category_folder_path)
        except (OSError, IOError) as e:
            print(f"Error when delete a folder {category_folder_path}: {e}")


@receiver(pre_delete, sender=Product)
def delete_product_images_folder(sender, instance, **kwargs):
    slug = instance.title.lower().replace(" ", "_").replace("/", "_").replace("-", "_")
    product_folder_path = os.path.join(settings.MEDIA_ROOT, "products", f"{instance.pk}_{slug}")

    if os.path.isdir(product_folder_path):
        try:
            shutil.rmtree(product_folder_path)
        except (OSError, IOError) as e:
            print(f"Error when delete a folder {product_folder_path}: {e}")