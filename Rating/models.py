from django.db import models
from django.contrib.auth.models import User
from products.models import Product

# Create your models here.


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, db_column="product")
    price_rating = models.FloatField(
        default=1, null=True, blank=True, db_column="price_rating")
    source_rating = models.FloatField(
        default=1, null=True, blank=True, db_column="source_rating")
    speed_rating = models.FloatField(
        default=1, null=True, blank=True, db_column="speed_rating")
    comment = models.CharField(
        max_length=255, null=True, blank=True, db_column="comment")
    created_on = models.DateTimeField(
        auto_now_add=True, db_column="created_on")

    class Meta:
        db_table = 'Rating'
        verbose_name_plural = 'Ratings'

    def __str__(self):
        return self.comment
