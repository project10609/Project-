from django.urls import path,re_path
from products.views import ProductDetailView,CategoryDetailView

app_name = 'products'

urlpatterns = [
    path('<int:pk>/',ProductDetailView.as_view(),name='product_detail'),
    path('category/<pk>/',CategoryDetailView.as_view(),name='categories')
]
