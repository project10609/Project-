from django.shortcuts import render
from .models import Rating

# Create your views here.


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    price_rating = Rating.objects.filter(
        product_name=product, rating_category="price_rating")
    source_rating = pass
    speed_rating = pass
