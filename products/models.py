from django.db import models
from django.http import HttpResponseRedirect
from django.urls import reverse, resolve
from django.db.models import Count
from Rating.models import Rating
from django.db.models import Count, Q, F, Sum, FloatField
from django.contrib.auth.models import User


class OrderItem(models.Model):
    product = models.OneToOneField('Product', on_delete=models.CASCADE, null=True, db_column='product')
    date_added = models.DateTimeField(auto_now=True,db_column='date_added')

    def __str__(self):
        return self.product.product_name

    class Meta:
        db_table = 'OrderItem'

class Order(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True,db_column='owner')
    items = models.ForeignKey(OrderItem,related_name='order',db_column='items',on_delete=models.CASCADE)

    def __str__(self):
        return self.items

    class Meta:
        db_table = 'Order'


class Categories(models.Model):
    name = models.CharField(max_length=120, db_column='name')
    slug = models.SlugField(unique=True, primary_key=True, db_column='slug')

    def __str__(self):
        return self.slug

    class Meta:
        db_table = 'CategoryList'
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return reverse('products:categories', kwargs={'pk': self.pk})
    #
    # def products_count(self):
    #     # Your filter criteria can go here.
    #     return self.products.count()


class Subcategories(models.Model):
    subcategory_name = models.CharField(max_length=120, db_column='name')
    slug = models.SlugField(unique=True, primary_key=True, db_column='slug')
    category = models.ForeignKey(
        Categories, db_column='category', on_delete=models.CASCADE, related_name='subcategory')

    def __str__(self):
        return self.slug

    class Meta:
        db_table = 'Subcategories'
        verbose_name_plural = 'Subcategories'

    def get_absolute_url(self):
        return reverse('products:subcategories', kwargs={'pk': self.pk})

    # def get_products_count(self):
    #     return self.subcategory.count()


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

    def get_rating(self):
        ratings = Rating.objects.filter(product=self.pk)
        price_rating = Rating.objects.filter(product=self.pk).aggregate(
            price_sum=Sum('price_rating', output_field=FloatField()) / Count('product', output_field=FloatField()))
        speed_rating = Rating.objects.filter(product=self.pk).aggregate(
            speed_sum=Sum('speed_rating', output_field=FloatField()) / Count('product', output_field=FloatField()))
        source_rating = Rating.objects.filter(product=self.pk).aggregate(
            source_sum=Sum('source_rating', output_field=FloatField()) / Count('product', output_field=FloatField()))
        if ratings:
            overall_rating = float((price_rating['price_sum'] +
                                    speed_rating['speed_sum'] + source_rating['source_sum'])) / 3
        else:
            overall_rating = int(0)
        return overall_rating

    def get_comment_count(self):
        return Rating.objects.filter(product=self.pk).aggregate(counts=Count('product')).get('counts')

    class Meta:
        db_table = 'Product'


class Source(models.Model):
    source = models.CharField(max_length=255, db_column='source')
    slug = models.SlugField(primary_key=True, db_column='slug')

    def __str__(self):
        return self.source

    class Meta:
        db_table = 'Source'
