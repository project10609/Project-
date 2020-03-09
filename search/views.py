from django.shortcuts import render
from products.models import Product,Categories
from django.db.models import Q
from django.http import HttpResponse
from django.views.generic import ListView,DetailView

# Create your views here.

# def search(request):
#     categories = Categories.objects.all()
#     if request.method == 'GET':
#         category = request.GET.get('category')
#         query = request.GET.get('q')
#         queryset = Product.objects.filter(product_name__icontains=query)
#         if category:
#             products = queryset.filter(product_category__name__contains=category)
#         return render(request,'search/search_result.html',{'products':products,'categories':categories})
#     else:
#         return render(request,'search/search_result.html',{'categories':categories})

class SearchListView(ListView):
    template_name = 'search/search_result.html'
    model = Product
    paginate_by = 25

    def get(self,request,*args,**kwargs):
        category = request.GET.get('category')
        query = request.GET.get('q')
        queryset = Product.objects.filter(product_name__icontains=query)
        self.results = queryset.filter(product_category__slug__exact=category)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        return super().get_context_data(results=self.results, **kwargs)
# def product_autocomplete(request, **kwargs):
#     term = request.GET.__getitem__('query')
#     products = [str(products) for products in    Product.objects.filter(Q(product_name__icontains=q))]
#     return HttpResponse(json.dumps(products))
