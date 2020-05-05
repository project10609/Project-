from django.urls import path, re_path
from products.views import category_item, subcategory, product_list, add_to_cart, cart_items,delete_cart_items
from Rating.views import product_detail, delete_rating,update_rating


app_name = 'products'

urlpatterns = [

    path('', product_list, name='allproduct'),
    path('following-list/',cart_items,name='following-list'),
    path('following-list/delete/<pk>',delete_cart_items,name='delete_cart'),
    path('<pk>/', product_detail, name='product_detail'),
    path('category/<pk>/', category_item, name='categories'),
    path('subcategory/<pk>/', subcategory, name='subcategory'),
    path('delete/<pk>/<id>/', delete_rating, name="delete_rating"),
    path('update/<pk>/<id>/', update_rating, name="update_rating"),
    path('add_to_cart/<pk>/<order>', add_to_cart, name="add_to_cart"),
    

    # path('category/<str:category>/<str:source>',source_sorting,name='source_sorting'),
]
