from django.contrib import admin
from django.utils.html import mark_safe
from .models import Collection, Author, Item, Tag

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'preview_cover')
    search_fields = ('name', 'description')
    readonly_fields = ('preview_cover',)

    def preview_cover(self, obj):
        return obj.preview_cover()
    preview_cover.short_description = "Обложка"


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        'surname',
        'name',
        'patronymic',
        'preview_photo',
    )
    list_display_links = ('surname', 'name', 'patronymic')
    search_fields = ('surname', 'name', 'patronymic')
    filter_horizontal = ('collections',)
    readonly_fields = ('preview_photo',)
    ordering = ('surname', 'name', 'patronymic')

    def preview_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="80" style="border-radius:4px;">')
        return "—"
    preview_photo.short_description = "Фото"


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_item_type_display', 'author', 'year', 'preview_image')
    list_filter = ('item_type', 'author', 'year')
    search_fields = ('title', 'description', 'author__surname', 'author__name')
    readonly_fields = ('preview_image',)

    def preview_image(self, obj):
        return obj.preview_image()
    preview_image.short_description = "Изображение"