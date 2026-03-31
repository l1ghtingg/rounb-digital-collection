from django.db import models
from django.utils.html import mark_safe
from ckeditor.fields import RichTextField


class Collection(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название коллекции")
    description = RichTextField(verbose_name="Описание", blank=True, null=True)
    cover_image = models.ImageField(
        upload_to='collections/%Y/%m/',
        verbose_name="Обложка коллекции",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Коллекция"
        verbose_name_plural = "Коллекции"
        ordering = ['name']

    def __str__(self):
        return self.name

    def preview_cover(self):
        if self.cover_image:
            return mark_safe(f'<img src="{self.cover_image.url}" width="120" style="object-fit:cover;">')
        return "—"
    preview_cover.short_description = "Обложка"


class Author(models.Model):
    surname = models.CharField(max_length=150, verbose_name="Фамилия")
    name = models.CharField(max_length=150, verbose_name="Имя")
    patronymic = models.CharField(max_length=150, blank=True, null=True, verbose_name="Отчество")
    def __str__(self):
        parts = [self.surname, self.name]
        if self.patronymic:
            parts.append(self.patronymic)
        return ' '.join(parts)

    photo = models.ImageField(
        upload_to='authors/',
        verbose_name="Фото автора",
        blank=True,
        null=True
    )
    biography = RichTextField(verbose_name="Биография", blank=True, null=True)

    collections = models.ManyToManyField(
        Collection,
        verbose_name="Коллекции",
        related_name="authors",
        blank=True
    )

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"
        ordering = ['surname', 'name']

    def __str__(self):
        return f"{self.surname} {self.name}".strip()

    def preview_photo(self):
        if self.photo:
            return mark_safe(f'<img src="{self.photo.url}" width="80" style="border-radius:50%;">')
        return "—"
    preview_photo.short_description = "Фото"


class Item(models.Model):
    TYPE_CHOICES = [
        ('autograph', 'Автограф'),
        ('book',      'Книга / издание'),
        ('cover',     'Обложка'),
        ('photo',     'Фотография'),
        ('other',     'Другое'),
    ]

    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Автор"
    )
    item_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        verbose_name="Тип материала"
    )
    title = models.CharField(max_length=300, verbose_name="Название / описание")
    description = RichTextField(verbose_name="Подробное описание", blank=True, null=True)
    year = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name="Год")
    image = models.ImageField(
        upload_to='items/%Y/%m/',
        verbose_name="Изображение",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Элемент коллекции"
        verbose_name_plural = "Элементы коллекции"
        ordering = ['-year', 'title']

    def __str__(self):
        return f"{self.get_item_type_display()}: {self.title[:60]}"

    def preview_image(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="120">')
        return "—"
    preview_image.short_description = "Изображение"

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название тега")
    slug = models.SlugField(max_length=100, unique=True, blank=True, verbose_name="Slug")

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ['name']

    def __str__(self):
        return self.name