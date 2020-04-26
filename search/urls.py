from django.urls import path
from search.views import search, search_from_home


app_name = 'search'

urlpatterns = [
    path('', search, name='search'),
    path('<pk>/', search_from_home, name='search_from_home'),
]
