from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from django.urls import reverse
from products.models import Product, Categories, Source, Subcategories
from django.views.generic import ListView, DetailView
from django.views.generic.list import MultipleObjectMixin
from .forms import ProductFilterForm, ProductSourceForm, ProductPriceForm
from django.db.models import Count


class CategoryMixin(object):
    def get_categories(self):
        return Categories.objects.all()

    def get_context_data(self, **kwargs):
        context = super(CategoryMixin, self).get_context_data(**kwargs)
        context['categories'] = self.get_categories()
        return context


class ProductListView(CategoryMixin, ListView):
    template_name = 'products/index.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 9

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total'] = self.get_queryset().count
        return context


class ProductDetailView(DetailView):
    template_name = 'products/productDetail.html'
    model = Product


def category_item(request, pk):
    category = get_object_or_404(Categories, pk=pk)

    products = Product.objects.filter(
        product_category__slug__icontains=category).order_by('?')
    if request.method == 'GET' and 'filter_by' in request.GET or request.method == 'GET' and 'source' in request.GET or request.method == 'GET' and 'min_price' in request.GET or request.method == 'GET' and 'max_price' in request.GET:
        sortingform = ProductFilterForm(request.GET)
        sourceform = ProductSourceForm(request.GET)
        priceform = ProductPriceForm(request.GET)
        if sortingform.is_valid() or sourceform.is_valid() or priceform.is_valid():
            min_price = request.GET.get('min_price', None)
            max_price = request.GET.get('max_price', None)
            source = request.GET.getlist('source', None)
            sortby = sortingform.cleaned_data.get('filter_by')
            if sortby == 'PriceAsc':
                if source:
                    if min_price and max_price:
                        products = products.filter(product_source__slug__in=source).filter(
                            product_price__range=(min_price, max_price)).order_by('product_price')
                    else:
                        products = products.filter(
                            product_source__slug__in=source).order_by('product_price')
                else:
                    if min_price and max_price:
                        products = products.filter(product_price__range=(
                            min_price, max_price)).order_by('product_price')
                    else:
                        products = products.order_by('product_price')
            elif sortby == 'PriceDesc':
                if source:
                    if min_price and max_price:
                        products = products.filter(product_source__slug__in=source).filter(
                            product_price__range=(min_price, max_price)).order_by('-product_price')
                    else:
                        products = products.filter(
                            product_source__slug__in=source).order_by('-product_price')
                else:
                    if min_price and max_price:
                        products = products.filter(product_price__range=(
                            min_price, max_price)).order_by('-product_price')
                    else:
                        products = products.order_by('-product_price')
            else:
                if source:
                    if min_price and max_price:
                        products = products.filter(product_source__slug__in=source).filter(
                            product_price__range=(min_price, max_price)).order_by('?')
                    else:
                        products = products.filter(
                            product_source__slug__in=source).order_by('?')
                else:
                    if min_price and max_price:
                        products = Product.objects.filter(product_category__slug__icontains=category).filter(
                            product_price__range=(min_price, max_price)).order_by('?')
                    else:
                        products = products.order_by('?')

        paginator = Paginator(products, 20)
        try:
            page = request.GET.get('page', '1')
        except:
            page = 1
        try:
            product_list = paginator.page(page)
        except(EmptyPage, InvalidPage):
            product_list = paginator.page(1)

        index = product_list.number - 1
        max_index = len(paginator.page_range)
        start_index = index - 5 if index >= 5 else 0
        end_index = index + 5 if index <= max_index - 5 else max_index
        page_range = list(paginator.page_range)[start_index:end_index]

        context = {
            'products': products,
            'product_list': product_list,
            'page_range': page_range,
            'category': category,
            'sortingform': sortingform,
            'sourceform': sourceform,
            'priceform': priceform,
        }
        return render(request, 'products/category_box.html', context)

    else:
        sortingform = ProductFilterForm()
        sourceform = ProductSourceForm()
        priceform = ProductPriceForm()

        paginator = Paginator(products, 20)
        try:
            page = request.GET.get('page', '1')
        except:
            page = 1
        try:
            product_list = paginator.page(page)
        except(EmptyPage, InvalidPage):
            product_list = paginator.page(1)

        index = product_list.number - 1
        max_index = len(paginator.page_range)
        start_index = index - 5 if index >= 5 else 0
        end_index = index + 5 if index <= max_index - 5 else max_index
        page_range = list(paginator.page_range)[start_index:end_index]

        context = {
            'products': products,
            'product_list': product_list,
            'page_range': page_range,
            'category': category,
            'sortingform': sortingform,
            'sourceform': sourceform,
            'priceform': priceform,
        }
        return render(request, 'products/category_box.html', context)


def subcategory(request, pk):
    category = get_object_or_404(Subcategories, pk=pk)
    products = Product.objects.filter(
        product_subcategory__slug__icontains=category).order_by('?')
    if request.method == 'GET' and 'filter_by' in request.GET or request.method == 'GET' and 'source' in request.GET or request.method == 'GET' and 'min_price' in request.GET or request.method == 'GET' and 'max_price' in request.GET:
        sortingform = ProductFilterForm(request.GET)
        sourceform = ProductSourceForm(request.GET)
        priceform = ProductPriceForm(request.GET)
        if sortingform.is_valid() or sourceform.is_valid() or priceform.is_valid():
            min_price = request.GET.get('min_price', None)
            max_price = request.GET.get('max_price', None)
            source = request.GET.getlist('source', None)
            sortby = sortingform.cleaned_data.get('filter_by')
            if sortby == 'PriceAsc':
                if source:
                    if min_price and max_price:
                        products = products.filter(product_source__slug__in=source).filter(
                            product_price__range=(min_price, max_price)).order_by('product_price')
                    else:
                        products = products.filter(
                            product_source__slug__in=source).order_by('product_price')
                else:
                    if min_price and max_price:
                        products = products.filter(product_price__range=(
                            min_price, max_price)).order_by('product_price')
                    else:
                        products = products.order_by('product_price')
            elif sortby == 'PriceDesc':
                if source:
                    if min_price and max_price:
                        products = products.filter(product_source__slug__in=source).filter(
                            product_price__range=(min_price, max_price)).order_by('-product_price')
                    else:
                        products = products.filter(
                            product_source__slug__in=source).order_by('-product_price')
                else:
                    if min_price and max_price:
                        products = products.filter(product_price__range=(
                            min_price, max_price)).order_by('-product_price')
                    else:
                        products = products.order_by('-product_price')
            else:
                if source:
                    if min_price and max_price:
                        products = products.filter(product_source__slug__in=source).filter(
                            product_price__range=(min_price, max_price)).order_by('?')
                    else:
                        products = products.filter(
                            product_source__slug__in=source).order_by('?')
                else:
                    if min_price and max_price:
                        products = Product.objects.filter(
                            product_price__range=(min_price, max_price)).order_by('?')
                    else:
                        products = products.order_by('?')

        paginator = Paginator(products, 20)
        try:
            page = request.GET.get('page', '1')
        except:
            page = 1
        try:
            product_list = paginator.page(page)
        except(EmptyPage, InvalidPage):
            product_list = paginator.page(1)

        index = product_list.number - 1
        max_index = len(paginator.page_range)
        start_index = index - 5 if index >= 5 else 0
        end_index = index + 5 if index <= max_index - 5 else max_index
        page_range = list(paginator.page_range)[start_index:end_index]

        context = {
            'products': products,
            'product_list': product_list,
            'page_range': page_range,
            'category': category,
            'sortingform': sortingform,
            'sourceform': sourceform,
            'priceform': priceform,
        }
        return render(request, 'products/subcategory.html', context)

    else:
        sortingform = ProductFilterForm()
        sourceform = ProductSourceForm()
        priceform = ProductPriceForm()

        paginator = Paginator(products, 20)
        try:
            page = request.GET.get('page', '1')
        except:
            page = 1
        try:
            product_list = paginator.page(page)
        except(EmptyPage, InvalidPage):
            product_list = paginator.page(1)

        index = product_list.number - 1
        max_index = len(paginator.page_range)
        start_index = index - 5 if index >= 5 else 0
        end_index = index + 5 if index <= max_index - 5 else max_index
        page_range = list(paginator.page_range)[start_index:end_index]

        context = {
            'products': products,
            'product_list': product_list,
            'page_range': page_range,
            'category': category,
            'sortingform': sortingform,
            'sourceform': sourceform,
            'priceform': priceform,
        }
        return render(request, 'products/subcategory.html', context)


def category_list(request):
    categories = Categories.objects.all()
    subcategory = Subcategories.objects.all()
    context = {
        "categories": categories,
        "subcategory": subcategory,
    }
    return context


def source_list(request):
    sources = Source.objects.all()
    context = {
        'sources': sources
    }
    return context
