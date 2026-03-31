from django.urls import path
from . import views
from django.views.generic import RedirectView

app_name = 'library'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('homepage', RedirectView.as_view(pattern_name='library:homepage', permanent=False)),
    path('collection/<int:pk>/', views.collection_detail, name='collection_detail'),
    path('author/<int:pk>/', views.author_detail, name='author_detail'),
    path('item/<int:pk>/', views.item_detail, name='item_detail'),
    path('search/', views.search, name='search'),
]