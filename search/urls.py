from django.urls import path
from search.views import search,search_by_source#SearchListView
app_name = 'search'

urlpatterns = [
    path('',search,name='search'),
    path('source',search_by_source,name='search_source')
]
