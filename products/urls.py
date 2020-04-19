from django.urls import path, re_path
from products.views import category_item, subcategory, product_list
from Rating.views import product_detail

app_name = 'products'

urlpatterns = [
    path('', product_list, name='allproduct'),
    path('<int:pk>/', product_detail, name='product_detail'),
    path('category/<pk>/', category_item, name='categories'),
    path('subcategory/<pk>', subcategory, name='subcategory')

    # path('category/<str:category>/<str:source>',source_sorting,name='source_sorting'),
]
