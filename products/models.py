from django.db import models
from django.http import HttpResponseRedirect
from django.urls import reverse


class Categories(models.Model):
    name = models.CharField(max_length=120, db_column='name')
    slug = models.SlugField(unique=True, primary_key=True, db_column='slug')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'CategoryList'
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return reverse('products:categories', kwargs={'pk': self.pk})


class Subcategories(models.Model):
    subcategory_name = models.CharField(max_length=120, db_column='name')
    slug = models.SlugField(unique=True, primary_key=True, db_column='slug')
    category = models.ForeignKey(
        Categories, db_column='category', on_delete=models.CASCADE, related_name='subcategory')

    def __str__(self):
        return self.subcategory_name

    class Meta:
        db_table = 'Subcategories'
        verbose_name_plural = 'Subcategories'

    def get_absolute_url(self):
        return reverse('products:subcategories', kwargs={'pk': self.pk})


class Product(models.Model):
    product_name = models.CharField(max_length=256, db_column='product_name')
    product_price = models.IntegerField(db_column='product_price')
    product_url = models.CharField(max_length=120, db_column='product_url')
    product_category = models.ForeignKey(
        Categories, db_column='product_category', on_delete=models.CASCADE, related_name='products')
    product_subcategory = models.ForeignKey(
        Subcategories, db_column='product_subcategory', on_delete=models.CASCADE, related_name="subcategory")
    product_images = models.CharField(
        max_length=120, db_column='product_images', blank=True, null=True)
    product_source = models.OneToOneField(
        'Source', db_column='product_source', on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        return reverse('products:product_detail', args=[self.pk])

    def get_success_url(self):
        return self.object.get_absolute_url + '?source=%s&filter_by=%s' % self.request.GET.get('source'), self.request.GET.get('filter_by')

    class Meta:
        db_table = 'Product'


class Source(models.Model):
    source = models.CharField(max_length=255, db_column='source')
    slug = models.SlugField(primary_key=True, db_column='slug')

    def __str__(self):
        return self.source

    class Meta:
        db_table = 'Source'
