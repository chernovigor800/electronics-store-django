from django.db import models
from django.db.models import Avg
from django.core.validators import MinValueValidator, MaxValueValidator

from smart_selects.db_fields import ChainedForeignKey

from reviews.models import Review


def category_image_directory_path(instance, filename):
    slug = instance.title.lower().replace(" ", "_").replace("/", "_").replace("-", "_")
    return f"categories/{instance.pk}_{slug}/image/{filename}"


class Category(models.Model):

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    title = models.CharField(max_length=200, db_index=True, verbose_name="Category")
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to=category_image_directory_path
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="children",
        null=True,
        blank=True,
        verbose_name="Parent category"
    )

    def get_image(self):
        if not self.image:
            return {
                "src": "/media/default_none.jpg",
                "alt": self.title
            }
        return {
            "src": self.image.url,
            "alt": self.title
        }

    def __str__(self):
        return self.title


class Tag(models.Model):

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Product(models.Model):

    class Meta:
        ordering = ['title', 'price']
        verbose_name = "Product"
        verbose_name_plural = "Products"

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products_parent')
    subcategory = ChainedForeignKey(
        Category,
        chained_field="category",
        chained_model_field="parent",
        show_all=False,
        blank=True,
        null=True,
    )
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    count = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    title = models.CharField(max_length=200, verbose_name="Product")
    description = models.TextField(null=False, blank=True)
    specification = models.ManyToManyField(
        "Specification", verbose_name="Specification", related_name="products"
    )
    freeDelivery = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, verbose_name="Tag", related_name="tags")

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
    )
    count_of_orders = models.IntegerField(default=0)

    def get_images(self):
        images = ProductImage.objects.filter(product_id=self.pk)

        if not images:
            return [
                {
                    "src": "/media/default_none.jpg",
                    "alt": "Default image"
                }
            ]

        return [
            {
                "src": image.image.url if image.image else "/media/default_none.jpg",
                "alt": image.image.name if image.image else "Missing image"
            }
            for image in images
        ]

    def get_rating(self):
        reviews = Review.objects.filter(product_id=self.pk).values_list(
            "rate", flat=True
        )
        if reviews.count() == 0:
            rating = 0
            return rating

        rating = sum(reviews) / reviews.count()
        return rating

    def update_rating(self):
        reviews = Review.objects.filter(product=self)
        if reviews.exists():
            avg_rating = reviews.aggregate(Avg('rate'))['rate__avg']
            self.rating = round(avg_rating, 2) if avg_rating else 0.00
        else:
            self.rating = 0.00
        self.save(update_fields=['rating'])

    def __str__(self):
        return self.title


def product_images_directory_path(instance, filename):
    product = instance.product
    slug = product.title.lower().replace(" ", "_").replace("/", "_").replace("-", "_")
    return f"products/{product.pk}_{slug}/images/{filename}"


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to=product_images_directory_path, default='/media/default_none.jpg', blank=True, null=True)


class Specification(models.Model):

    class Meta:
        verbose_name = "Specification"
        verbose_name_plural = "Specifications"

    name = models.CharField(max_length=50, blank=True, null=True)
    value = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.name}: {self.value}"