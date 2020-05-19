from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404,redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from django.urls import reverse
from products.models import Product, Categories, Source, Subcategories, Order, OrderItem
from django.views.generic import ListView, DetailView
from django.views.generic.list import MultipleObjectMixin
from .forms import ProductFilterForm, ProductSourceForm, ProductPriceForm
from django.db.models import Count, Q
from search.models import Queries
from functools import reduce
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import operator
import random
import os
from django.contrib.auth.models import User

# class Products(ListView):
#     template = ""


class CategoryMixin(object):
    def get_categories(self):
        return Categories.objects.all()

    def get_context_data(self, **kwargs):
        context = super(CategoryMixin, self).get_context_data(**kwargs)
        context['categories'] = self.get_categories()
        return context


def index(request):

    products = Product.objects.all()
    queries_items = list(Queries.objects.values_list(
        'search', flat=True).annotate(counts=Count('search')).distinct())
    queries = Queries.objects.all().values(
        'search').annotate(counts=Count('search')).order_by('-counts')[:10]
    listitems = list(Queries.objects.values_list(
        'search', flat=True).distinct().filter(user=request.user.id))

    if queries_items and not listitems:
        recommendItems = products.filter(
            reduce(operator.or_, (Q(product_name__icontains=x['search']) for x in queries)))[:10]
        context = {
            'queries': queries,
            'recommendItems': recommendItems,
        }
        return render(request, 'products/index.html', context)
    elif listitems and not queries_items:
        products = products.filter(
            reduce(operator.or_, (Q(product_name__icontains=x) for x in listitems)))[:10]
        context = {
            'queries': queries,
            'user_item': products,
        }

        return render(request, 'products/index.html', context)
    elif queries_items and listitems:
        recommendItems = products.filter(
            reduce(operator.or_, (Q(product_name__icontains=x['search']) for x in queries)))[:10]
        products = products.filter(
            reduce(operator.or_, (Q(product_name__icontains=x) for x in listitems)))[:10]
        context = {
            'queries': queries,
            'recommendItems': recommendItems,
            'user_item': products,
        }

        return render(request, 'products/index.html', context)
    else:
        return render(request, 'products/index.html', {})


def product_list(request):
    products = Product.objects.all().order_by('?')
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
            'sortingform': sortingform,
            'sourceform': sourceform,
            'priceform': priceform,

        }
        return render(request, 'products/Productlist.html', context)

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
            'sortingform': sortingform,
            'sourceform': sourceform,
            'priceform': priceform,

        }
        return render(request, 'products/Productlist.html', context)


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
        return render(request, 'products/category.html', context)

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
        return render(request, 'products/category.html', context)


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



# def product_


def category_list(request):
    categories = Categories.objects.all()
    subcategory = Subcategories.objects.all()
    if request.user.is_authenticated:
        order_list = Order.objects.filter(owner=request.user)
        orders_count = Order.objects.filter(owner=request.user).aggregate(order_counts=Count('items')).get('order_counts')
        context = {
        "categories": categories,
        "subcategory": subcategory,
        'orders_count':orders_count,
        'order_list':order_list,
        }
    else:
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


@login_required
def add_to_cart(request,pk,order):
  
    #get the user 
    user_profile = get_object_or_404(User, pk=pk)
    product = get_object_or_404(Product,pk=order)
    
    if Order.objects.filter(items__product=product,owner=request.user):
        messages.error(request,"此商品已經在追蹤清單裡")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
    else:
        cart_item = OrderItem.objects.create(product=product)
        Order.objects.get_or_create(owner=user_profile,items=cart_item)

        messages.success(request, "商品成功加入追蹤清單")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

@login_required
def cart_items(request):
    orders = Order.objects.filter(owner=request.user)
    context = {
        'orders':orders,
    }
    return render(request,'products/following-list.html',context)

@login_required
def delete_cart_items(request,pk):
    cart_items = get_object_or_404(Order,pk=pk).delete()
    messages.success(request,'此商品成功從追蹤清單裡移除')
    return redirect(reverse('products:following-list'))

@login_required
def delete_all(request):
    product = Product.objects.all()
    cart_items = Order.objects.filter(owner=request.user).delete()
    cart_items.filter(items__product=product).delete()
    messages.success(request,'追蹤清單刪除成功')
    return redirect(request.META.get('HTTP_REFERER','/'))