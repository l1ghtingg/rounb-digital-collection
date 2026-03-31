from django.shortcuts import render, get_object_or_404
from .models import Collection, Author, Item
from django.db.models import Q

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

def search(request):
    query = request.GET.get('q', '').strip()
    results_authors = []
    results_items = []

    if query:
        # Поиск по авторам
        results_authors = Author.objects.filter(
            Q(surname__icontains=query) |
            Q(name__icontains=query) |
            Q(patronymic__icontains=query)
        ).distinct()

        # Поиск по элементам (название и описание)
        results_items = Item.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        ).select_related('author')

    context = {
        'query': query,
        'results_authors': results_authors,
        'results_items': results_items,
    }
    return render(request, 'library/search.html', context)