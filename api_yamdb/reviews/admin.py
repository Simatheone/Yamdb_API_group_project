from django.contrib import admin

from reviews.models import Categories, Genres, Titles
from api_yamdb.settings import EMPTY_VALUE_ADMIN_PANEL


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    """Админ панель для модели Категории."""
    list_display = ('pk', 'name', 'slug')
    list_editable = ('name',)
    list_filter = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    empty_value_display = EMPTY_VALUE_ADMIN_PANEL


@admin.register(Genres)
class GenresAdmin(admin.ModelAdmin):
    """Админ панель для модели Жанры."""
    list_display = ('pk', 'name', 'slug')
    list_editable = ('name',)
    list_filter = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    empty_value_display = EMPTY_VALUE_ADMIN_PANEL


@admin.register(Titles)
class TitlesAdmin(admin.ModelAdmin):
    """Админ панель для модели Произведения."""
    list_display = ('pk', 'name', 'year', 'description', 'category')
    list_editable = ('name', 'year', 'description', 'category')
    list_filter = ('name', 'year', 'category')
    empty_value_display = EMPTY_VALUE_ADMIN_PANEL
