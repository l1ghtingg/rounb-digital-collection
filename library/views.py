from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Collection, Author, Item, Tag   # Tag добавь после создания модели
from datetime import datetime

def homepage(request):
    collections = Collection.objects.all().order_by('name')
    tags = Tag.objects.all()
    current_year = datetime.now().year
    
    return render(request, 'library/homepage.html', {
        'collections': collections,
        'tags': tags,
        'current_year': current_year,
    })

def search(request):
    query = request.GET.get('q', '').strip()
    tag_slug = request.GET.get('tag', '')
    year = request.GET.get('year', '')

    results_authors = Author.objects.none()
    results_items = Item.objects.none()

    if query:
        # Поиск по авторам
        results_authors = Author.objects.filter(
            Q(surname__icontains=query) |
            Q(name__icontains=query) |
            Q(patronymic__icontains=query)
        ).distinct()

        # Поиск по материалам
        results_items = Item.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        ).select_related('author')

    # Фильтрация по тегу
    if tag_slug:
        if tag_slug == 'юбиляры' and year:
            # Специальный режим "Юбиляры"
            results_items = Item.objects.filter(year=year)
        else:
            results_items = results_items.filter(tags__slug=tag_slug)

    context = {
        'query': query,
        'tag_slug': tag_slug,
        'year': year,
        'results_authors': results_authors,
        'results_items': results_items,
        'tags': Tag.objects.all(),
    }
    return render(request, 'library/search.html', context)

def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    items = author.items.all().order_by('-year', 'title')
    return render(request, 'library/author_detail.html', {
        'author': author,
        'items': items,
    })