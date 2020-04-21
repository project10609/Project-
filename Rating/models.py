from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404

# Create your models here.


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user")
    product = models.ForeignKey(
        to='products.Product', on_delete=models.CASCADE, db_column="product", related_name="rating")
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
