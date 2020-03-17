from django.shortcuts import render
from products.models import Product,Categories
from django.db.models import Q
from django.http import HttpResponse
from django.views.generic import ListView,DetailView
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
# Create your views here.

def search(request):
    category = request.GET.get('category',None)
    query = request.GET.get('q',None)
    if category:
        products = Product.objects.filter(product_category__name__contains=category).filter(product_name__icontains=query)
    elif category == "":
        products = Product.objects.filter(product_name__icontains=query)
    paginator = Paginator(products, 10) # Show 10 contacts per page.
    page = request.GET.get('page',1)

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    total = products.count()

    return render(request,'search/search_result.html',{'page_obj':page_obj,'total':total})

def search_by_source(request):
    source = request.GET.getlist('sourcecheck[]')
    products = Product.objects.filter(product_source__slug__icontains=source)
    paginator = Paginator(products, 10) # Show 10 contacts per page.
    page = request.GET.get('page',1)

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    total = products.count()

    return render(request,'search/search_result_by_source.html',{'page_obj':page_obj,'total':total})

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
