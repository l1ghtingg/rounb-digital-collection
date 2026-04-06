from django.urls import path
from . import views

app_name = 'library'

urlpatterns = [
    path('', views.homepage, name='homepage'),           # Главная страница
    path('author/<int:pk>/', views.author_detail, name='author_detail'),
    path('search/', views.search, name='search'),
]