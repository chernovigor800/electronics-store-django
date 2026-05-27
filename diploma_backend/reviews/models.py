from django.db import models
from django.core.validators import MaxValueValidator

from accounts.models import ProfileUser


class Review(models.Model):

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

    author = models.ForeignKey(ProfileUser, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    product = models.ForeignKey(
        'products.Product', on_delete=models.CASCADE,
        verbose_name="Product", related_name="reviews"
    )
    rate = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(5)], verbose_name="Rating"
    )
    review_author_name = models.CharField(max_length=255, blank=True)  # ✅ Новое!
    review_author_email = models.EmailField(blank=True)


    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        self.product.update_rating()

    def __str__(self):
        return f"{self.product.title} - {self.rate}/5"


