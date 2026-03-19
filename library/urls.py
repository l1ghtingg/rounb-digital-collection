from django.urls import path
from . import views

app_name = 'library'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('collection/<int:pk>/', views.collection_detail, name='collection_detail'),
    path('author/<int:pk>/', views.author_detail, name='author_detail'),
    path('item/<int:pk>/', views.item_detail, name='item_detail'),
]
