from django.urls import path
from search.views import search_emp, el_search

urlpatterns = [
    path('', el_search, name='search')
]
