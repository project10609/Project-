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
from django.db.models import Count, Q, F, Sum, FloatField
from search.models import Queries
from functools import reduce
import operator
import random
import os
from django.db.models.functions import Cast
from .forms import RatingForm, RatingUpdateForm
from django.contrib import messages
from django.utils import timezone
from django.views.generic.edit import UpdateView
from django.contrib.auth.models import User
# Create your views here.


user = User.objects.all()


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    ratings = Rating.objects.filter(product=product).annotate(
        user_rating=(F('price_rating') + F('speed_rating') + F('source_rating')) / 3)
    price_rating = Rating.objects.filter(product=product).aggregate(
        price_sum=Sum('price_rating', output_field=FloatField()) / Count('product', output_field=FloatField()))
    speed_rating = Rating.objects.filter(product=product).aggregate(
        speed_sum=Sum('speed_rating', output_field=FloatField()) / Count('product', output_field=FloatField()))
    source_rating = Rating.objects.filter(product=product).aggregate(
        source_sum=Sum('source_rating', output_field=FloatField()) / Count('product', output_field=FloatField()))
    if ratings:
        overall_rating = float((price_rating['price_sum'] +
                                speed_rating['speed_sum'] + source_rating['source_sum'])) / 3
    else:
        overall_rating = int(0)

    if request.method == "POST":
        form = RatingForm(request.POST)
        if form.is_valid:
            price_comment = request.POST.get('price_rating', None)
            speed_comment = request.POST.get('source_rating', None)
            source_comment = request.POST.get('speed_rating', None)
            comment = request.POST.get('comment', None)
            new_comment = Rating.objects.create(user=request.user, product=product, price_rating=price_comment,
                                                speed_rating=speed_comment, source_rating=source_comment, comment=comment, created_on=timezone.now())
            new_comment.save()
            messages.success(request, '成功新增評價！')

    else:
        form = RatingForm()

    comment_count = ratings.aggregate(counts=Count('product')).get('counts')

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
        'form': form,
        'overall_rating': overall_rating,
        'price_rating': price_rating,
        'speed_rating': speed_rating,
        'source_rating': source_rating,
        'product': product,
        'ratings': rating_list,
        'comment_count': comment_count,
        'rating_list': rating_list,
    }
    return render(request, 'products/product_detail.html', context)


def delete_rating(request, pk, id):
    product = get_object_or_404(Product, pk=pk)
    rating = Rating.objects.get(pk=id).delete()
    messages.success(request, "刪除成功！")
    return HttpResponseRedirect(reverse('products:product_detail', args=(product.pk,)))


def update_rating(request, pk, id):
    product = Product.objects.get(pk=pk)
    rating = Rating.objects.get(pk=id)
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid:
            form = RatingForm(request.POST, instance=rating)
            form.save()
            messages.success(request, '評價更改成功')
    else:
        form = RatingForm()

    return render(request, 'Rating/rating_update.html', {'form': form, 'product': product, })


# class UpdateRating(UpdateView):
#     model = Rating
#     form_class = RatingForm
#     template_name = 'Rating/rating_update.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(UpdateRating, self).get_context_data(**kwargs)
#         context['product'] = Product.objects.get(pk=)
#         return context
