from datetime import datetime

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from .models import Author, Collection, Item, Tag


def get_anniversary_info(author, year):
    anniversaries = []

    if author.birth_date:
        age = year - author.birth_date.year
        if age >= 75 and age % 5 == 0:
            anniversaries.append({
                'value': age,
                'event_date': author.birth_date.replace(year=year),
                'label': f'{age} лет со дня рождения',
            })

    anniversaries.sort(key=lambda x: (x['event_date'].month, x['event_date'].day))
    return anniversaries

def homepage(request):
    collections = Collection.objects.all().order_by('name')
    all_tags = Tag.objects.all().order_by('name')

    return render(request, 'library/homepage.html', {
        'collections': collections,
        'all_tags': all_tags,
        'current_year': datetime.now().year,
    })


def search(request):
    query = request.GET.get('q', '').strip()
    tag_slug = request.GET.get('tag')
    year_str = request.GET.get('year', '').strip()
    letter = request.GET.get('letter', '').strip()

    results_authors = Author.objects.none()
    results_items = Item.objects.none()
    selected_tag = None
    year = None

    if year_str.isdigit():
        year = int(year_str)

    if tag_slug:
        selected_tag = Tag.objects.filter(slug=tag_slug).first()
        results_authors = Author.objects.filter(tags__slug=tag_slug).distinct()
        results_items = Item.objects.none()

        if tag_slug == 'yubilyary' and year:
            filtered_authors = []

            for author in results_authors:
                anniversaries = get_anniversary_info(author, year)
                if anniversaries:
                    author.anniversaries = anniversaries
                    author.main_anniversary = anniversaries[0]
                    filtered_authors.append(author)

            filtered_authors.sort(
                key=lambda a: (
                    a.main_anniversary['event_date'].month,
                    a.main_anniversary['event_date'].day,
                    a.surname or '',
                    a.name or '',
                    a.patronymic or '',
                )
            )
            results_authors = filtered_authors

    if letter:
        results_authors = Author.objects.filter(
            surname__istartswith=letter
        ).distinct()
        results_items = Item.objects.none()

    if query:
        normalized_query = query.casefold()

        matched_authors = []
        for author in Author.objects.all():
            full_name_parts = [
                author.surname or '',
                author.name or '',
                author.patronymic or '',
            ]
            full_name = ' '.join(full_name_parts).casefold()

            if normalized_query in full_name:
                matched_authors.append(author.id)

        author_query = Author.objects.filter(id__in=matched_authors).distinct()
        item_query = Item.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        ).select_related('author').distinct()

        if tag_slug:
            if isinstance(results_authors, list):
                existing_ids = [author.id for author in results_authors]
                extra_authors = list(author_query.exclude(id__in=existing_ids))

                if tag_slug == 'yubilyary' and year:
                    prepared_extra = []
                    for author in extra_authors:
                        anniversaries = get_anniversary_info(author, year)
                        if anniversaries:
                            author.anniversaries = anniversaries
                            author.main_anniversary = anniversaries[0]
                            prepared_extra.append(author)
                    extra_authors = prepared_extra

                results_authors = results_authors + extra_authors
            else:
                results_authors = (results_authors | author_query).distinct()

            results_items = (results_items | item_query).distinct()
        else:
            results_authors = author_query
            results_items = item_query

    authors_count = (
        len(results_authors)
        if isinstance(results_authors, list)
        else results_authors.count()
    )

    context = {
        'query': query,
        'letter': letter,
        'tag_slug': tag_slug,
        'selected_tag': selected_tag,
        'results_authors': results_authors,
        'results_items': results_items,
        'authors_count': authors_count,
        'items_count': results_items.count(),
        'current_year': datetime.now().year,
        'year': year,
    }

    return render(request, 'library/search.html', context)


def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    items = author.items.prefetch_related('gallery_images').all().order_by('-year', 'title')

    return render(request, 'library/author_detail.html', {
        'author': author,
        'items': items,
    })


def autocomplete_authors(request):
    term = request.GET.get('term', '').strip()
    results = []

    if term:
        normalized_term = term.casefold()
        matched_authors = []

        for author in Author.objects.all():
            surname = (author.surname or '').casefold()
            name = (author.name or '').casefold()
            patronymic = (author.patronymic or '').casefold()

            if (
                surname.startswith(normalized_term) or
                name.startswith(normalized_term) or
                patronymic.startswith(normalized_term)
            ):
                matched_authors.append(author)

        for author in matched_authors[:10]:
            results.append({
                'id': author.id,
                'label': str(author),
                'url': f'/author/{author.id}/',
            })

    return JsonResponse({'results': results})


def collection_detail(request, pk):
    collection = get_object_or_404(Collection, pk=pk)
    authors = collection.authors.all().order_by('surname', 'name', 'patronymic')

    return render(request, 'library/collection_detail.html', {
        'collection': collection,
        'authors': authors,
        'current_year': datetime.now().year,
    })