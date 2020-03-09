from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import *
from django.core.paginator import Paginator
from django.urls import reverse
from products.models import Product,Categories
from django.views.generic import ListView,DetailView
from django.views.generic.list import MultipleObjectMixin


class CategoryMixin(object):
    def get_categories(self):
        return Categories.objects.all()

    def get_context_data(self, **kwargs):
        context = super(CategoryMixin, self).get_context_data(**kwargs)
        context['categories'] = self.get_categories()
        return context


class ProductListView(CategoryMixin,ListView):
    template_name = 'products/index.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 25


class ProductDetailView(DetailView):
    template_name = 'products/productDetail.html'
    model = Product

#
class CategoryDetailView(DetailView):
    template_name = 'products/category.html'
    model = Categories
    context_object_name = 'category'
    paginate_by = 10

    

def category_list(request):
    categories = Categories.objects.all()
    context = {
        "categories": categories,
    }
    return context
