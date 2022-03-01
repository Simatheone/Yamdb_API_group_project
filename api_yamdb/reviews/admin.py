from django.contrib import admin
from django.conf import settings

from reviews.models import Categories, CustomUser, Genres, Titles
from api_yamdb.settings import EMPTY_VALUE_ADMIN_PANEL


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "bio",
        "role",
        "is_staff",
    )
    search_fields = ("username",)
    list_filter = ("role",)
    empty_value_display = settings.EMPTY_VALUE_ADMIN_PANEL


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
