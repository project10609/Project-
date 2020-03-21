from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import *
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger,InvalidPage
from django.urls import reverse
from products.models import Product,Categories,Source
from django.views.generic import ListView,DetailView
from django.views.generic.list import MultipleObjectMixin
from .forms import ProductFilterForm,ProductSourceForm

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
    paginate_by = 9

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total'] = self.get_queryset().count
        return context


class ProductDetailView(DetailView):
    template_name = 'products/productDetail.html'
    model = Product

def category_item(request,pk):
    category = get_object_or_404(Categories,pk=pk)
    products = Product.objects.filter(product_category__slug__icontains=category).order_by('?')
    if request.method == 'GET' and 'filter_by' in request.GET or request.method == 'GET' and 'source' in request.GET:
        sortingform = ProductFilterForm(request.GET)
        sourceform = ProductSourceForm(request.GET)
        if sortingform.is_valid() or sourceform.is_valid():
            source = request.GET.getlist('source', None)
            sortby = sortingform.cleaned_data.get('filter_by')
            if sortby == 'PriceAsc':
                products = products.filter(product_source__slug__in=source).order_by('product_price')
            elif sortby == 'PriceDesc':
                products = products.filter(product_source__slug__in=source).order_by('-product_price')
            else:
                products = products.filter(product_source__slug__in=source)


        paginator = Paginator(products,20)
        try:
            page = request.GET.get('page','1')
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

        context={
            'products':products,
            'product_list':product_list,
            'page_range':page_range,
            'category':category,
            'sortingform':sortingform,
            'sourceform':sourceform
        }
        return render(request,'products/category.html',context)

    else:
        sortingform = ProductFilterForm()
        sourceform = ProductSourceForm()

        paginator = Paginator(products,20)
        try:
            page = request.GET.get('page','1')
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

        context={
            'products':products,
            'product_list':product_list,
            'page_range':page_range,
            'category':category,
            'sortingform':sortingform,
            'sourceform':sourceform
        }
        return render(request,'products/category.html',context)

def source_sorting(request,category,source):
    category = get_object_or_404(Categories,pk=category)
    sources = get_object_or_404(Source,source=source)
    products = Product.objects.filter(product_category__slug__icontains=category).filter(product_source__slug__icontains=sources)
    sourceform = ProductSourceForm(request.GET)

    if request.method == 'GET' and 'source' in request.GET:
        source = request.GET.getlist('source')
        products = products.filter(product_source__slug__icontains=source)

    paginator = Paginator(products,25)
    try:
        page = request.GET.get('page','1')
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

    context={
        'sourceform':sourceform,
        'products':products,
        'product_list':product_list,
        'page_range':page_range,
        'category':category,
        'sources':sources
    }
    return render(request,'products/source_sorting.html',context)



def category_list(request):
    categories = Categories.objects.all()
    context = {
        "categories": categories,
    }
    return context

def source_list(request):
    sources = Source.objects.all()
    context = {
        'sources':sources
    }
    return context
