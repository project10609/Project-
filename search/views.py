from django.shortcuts import render
from products.models import Product,Categories
from .models import Queries
from django.db.models import Q
from django.http import HttpResponse
from django.views.generic import ListView,DetailView
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
# Create your views here.

def search(request):
    category = request.GET.get('category',None)
    query = request.GET.get('q',None)
    if category:
        products = Product.objects.filter(product_category__slug__icontains=category).filter(product_name__icontains=query)
        result = Queries.objects.create(search=query,user=request.user)
        result.save()
    if category == "":
        products = Product.objects.filter(product_name__icontains=query)
        result = Queries.objects.create(search=query,user=request.user)
        result.save()


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

    total = products.count()

    context = {
        'product_list':product_list,
        'total':total,
        'page_range':page_range,

    }

    return render(request,'search/search_result.html',context)



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
