from django.shortcuts import render
from .models import Rating
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from django.urls import reverse
from products.models import Product, Categories, Source, Subcategories
from django.views.generic import ListView, DetailView
from django.views.generic.list import MultipleObjectMixin
from products.forms import ProductFilterForm, ProductSourceForm, ProductPriceForm
from django.db.models import Count, Q
from search.models import Queries
from functools import reduce
import operator
import random
import os

# Create your views here.


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    ratings = Rating.objects.filter(product=product)
    comment_count = ratings.aggregate(counts=Count('comment')).get('counts')

    paginator = Paginator(ratings, 4)
    try:
        page = request.GET.get('page', '1')
    except:
        page = 1
    try:
        rating_list = paginator.page(page)
    except(EmptyPage, InvalidPage):
        rating_list = paginator.page(1)

    index = rating_list.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 5 if index >= 5 else 0
    end_index = index + 5 if index <= max_index - 5 else max_index
    page_range = list(paginator.page_range)[start_index:end_index]

    context = {
        'product': product,
        'ratings': rating_list,
        'comment_count': comment_count,
    }
    return render(request, 'products/product_detail.html', context)
