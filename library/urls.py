from django.urls import path
from . import views

app_name = 'library'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('author/<int:pk>/', views.author_detail, name='author_detail'),
    path('collection/<int:pk>/', views.collection_detail, name='collection_detail'),
    path('search/', views.search, name='search'),
    path('autocomplete-authors/', views.autocomplete_authors, name='autocomplete_authors'),
]