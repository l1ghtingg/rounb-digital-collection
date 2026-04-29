from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Collection, Author, Item, Tag
from datetime import datetime


def homepage(request):
    collections = Collection.objects.all().order_by('name')
    all_tags = Tag.objects.all().order_by('name')

    return render(request, 'library/homepage.html', {
        'collections': collections,
        'all_tags': all_tags,
        'current_year': 2026,
    })


def search(request):
    query = request.GET.get('q', '').strip()
    tag_slug = request.GET.get('tag')
    year_str = request.GET.get('year')

    results_authors = Author.objects.none()
    results_items = Item.objects.none()
    selected_tag = None

    if tag_slug:
        selected_tag = Tag.objects.filter(slug=tag_slug).first()

        results_authors = Author.objects.filter(
            tags__slug=tag_slug
        ).distinct()

        results_items = Item.objects.filter(
            tags__slug=tag_slug
        ).select_related('author').distinct()

        # Логика для юбиляров
        if tag_slug == 'yubilyary' and year_str and year_str.isdigit():
            year = int(year_str)

            # Оставляем только тех авторов,
            # у кого юбилейная дата (75+, кратно 5)
            results_authors = [
                author for author in results_authors
                if author.birth_year
                and (year - author.birth_year) >= 75
                and (year - author.birth_year) % 5 == 0
            ]

            # Материалы только этих авторов
            results_items = results_items.filter(
                author__in=results_authors
            )

            print(
                f"Юбиляры {year} года → "
                f"Авторов: {len(results_authors)} | "
                f"Материалов: {results_items.count()}"
            )

    # Обычный текстовый поиск
    if query:
        author_query = Author.objects.filter(
            Q(surname__istartswith=query) |
            Q(name__istartswith=query) |
            Q(patronymic__istartswith=query)
        ).distinct()

        item_query = Item.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        ).select_related('author').distinct()

        if tag_slug:
            # Если results_authors уже list (например юбиляры)
            if isinstance(results_authors, list):
                existing_ids = [author.id for author in results_authors]

                extra_authors = author_query.exclude(
                    id__in=existing_ids
                )

                results_authors = results_authors + list(extra_authors)
            else:
                results_authors = (
                    results_authors | author_query
                ).distinct()

            results_items = (
                results_items | item_query
            ).distinct()

        else:
            results_authors = author_query
            results_items = item_query

    context = {
        'query': query,
        'tag_slug': tag_slug,
        'selected_tag': selected_tag,

        'results_authors': results_authors,
        'results_items': results_items,

        'authors_count': (
            len(results_authors)
            if isinstance(results_authors, list)
            else results_authors.count()
        ),

        'items_count': results_items.count(),

        'current_year': datetime.now().year,
    }

    return render(
        request,
        'library/search.html',
        context
    )


def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    items = author.items.all().order_by('-year', 'title')

    return render(request, 'library/author_detail.html', {
        'author': author,
        'items': items,
    })