from django.shortcuts import render
from products.models import Product, Categories
from .models import Queries
from django.db.models import Q
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from django.contrib.auth.models import User
from products.forms import ProductFilterForm, ProductPriceForm, ProductSourceForm
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from functools import reduce
import operator
import os

# Create your views here.


def search(request):
    category = request.GET.get('category', None)
    query = request.GET.get('q', None)
    if category:
        if request.user.is_authenticated:
            result = Queries.objects.create(search=query,user= request.user)
            result.save()
        else:
            result = Queries.objects.create(search=query)
            result.save()
        products = Product.objects.filter(
            product_category__slug__icontains=category).filter(product_name__icontains=query)
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
                'product_list': product_list,

                'page_range': page_range,
                'category': category,
                'sortingform': sortingform,
                'sourceform': sourceform,
                'priceform': priceform,
            }

            return render(request, 'search/search_result.html', context)

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
            return render(request, 'search/search_result.html', context)

    if category == "":

        products = Product.objects.filter(product_name__icontains=query)
        if request.user.is_authenticated:
            result = Queries.objects.create(search=query,user= request.user)
            result.save()
        else:
            result = Queries.objects.create(search=query)
            result.save()
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
                'product_list': product_list,

                'page_range': page_range,
                'category': category,
                'sortingform': sortingform,
                'sourceform': sourceform,
                'priceform': priceform,
            }

            return render(request, 'search/search_result.html', context)

        else:
            sortingform = ProductFilterForm()
            sourceform = ProductSourceForm()
            priceform = ProductPriceForm()
            products = products.annotate(total_count=Count('product_name'))

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
            return render(request, 'search/search_result.html', context)

    else:
        products = Product.objects.filter(product_name__icontains=query)
        if request.user.is_authenticated:
            result = Queries.objects.create(search=query,user= request.user)
            result.save()
        else:
            result = Queries.objects.create(search=query)
            result.save()
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
                'product_list': product_list,

                'page_range': page_range,
                'category': category,
                'sortingform': sortingform,
                'sourceform': sourceform,
                'priceform': priceform,
            }

            return render(request, 'search/search_result.html', context)

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
            return render(request, 'search/search_result.html', context)


def search_from_home(request, pk):
    products = Product.objects.filter(product_name__icontains=pk)
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
                        products = products.filter(
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
            'product_list': product_list,
            'page_range': page_range,
            'sortingform': sortingform,
            'sourceform': sourceform,
            'priceform': priceform,
        }

        return render(request, 'search/searchfromhome.html', context)

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
        return render(request, 'search/searchfromhome.html', context)


# class SearchListView(ListView):
#     template_name = 'search/search_result.html'
#     paginate_by = 10
#
#     def get_queryset(self):
#         return Product.objects.filter(product_name__icontains=request.GET['q'],product_category__slug__iexact=request.GET['category'])
#
#     def get(self,request,*args,**kwargs):
#         category = request.GET.get('category')
#         self.query = request.GET.get('q')
#         queryset1 = Product.objects.filter(product_name__icontains=self.query)
#         self.results = queryset1.filter(product_category__slug__exact=category)
#         return super().get(request, *args, **kwargs)
#
#     def get_context_data(self, **kwargs):
#         return super().get_context_data(results=self.results,query=self.query, **kwargs)
# def product_autocomplete(request, **kwargs):
#     term = request.GET.__getitem__('query')
#     products = [str(products) for products in    Product.objects.filter(Q(product_name__icontains=q))]
#     return HttpResponse(json.dumps(products))
