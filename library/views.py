from django.shortcuts import render, get_object_or_404
from .models import Collection, Author, Item

def homepage(request):
    collections = Collection.objects.all().order_by('name')
    return render(request, 'library/homepage.html', {
        'collections': collections,
    })

def collection_detail(request, pk):
    collection = get_object_or_404(Collection, pk=pk)
    authors = collection.authors.all().order_by('surname', 'name')
    return render(request, 'library/collection_detail.html', {
        'collection': collection,
        'authors': authors,
    })

def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    items = author.items.all().order_by('-year', 'title')
    return render(request, 'library/author_detail.html', {
        'author': author,
        'items': items,
    })

def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'library/item_detail.html', {
        'item': item,
    })