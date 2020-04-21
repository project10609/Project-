from django.urls import path, re_path
from products.views import category_item, subcategory, product_list
from Rating.views import product_detail, delete_rating, update_rating


app_name = 'products'

urlpatterns = [

    path('', product_list, name='allproduct'),
    path('<pk>/', product_detail, name='product_detail'),
    path('category/<pk>/', category_item, name='categories'),
    path('subcategory/<pk>/', subcategory, name='subcategory'),
    path('delete/<pk>/<id>/', delete_rating, name="delete_rating"),
    path('<int:pk>/<int:id>/update/',
         update_rating, name="update_rating"),


    # path('category/<str:category>/<str:source>',source_sorting,name='source_sorting'),
]
