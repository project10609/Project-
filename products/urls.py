from django.urls import path, re_path
from products.views import ProductDetailView, category_item, subcategory

app_name = 'products'

urlpatterns = [
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('category/<pk>/', category_item, name='categories'),
    path('subcategory/<pk>', subcategory, name='subcategory')
    # path('category/<str:category>/<str:source>',source_sorting,name='source_sorting'),
]
