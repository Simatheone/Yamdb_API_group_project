from django.contrib import admin

from api_yamdb.settings import EMPTY_VALUE_ADMIN_PANEL

from .models import Category, Comment, CustomUser, Genre, Review, Title


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    """Админ панель для модели Кастомного Юзера."""
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'role',
        'is_staff',
    )
    search_fields = ('username',)
    list_filter = ('role',)
    empty_value_display = EMPTY_VALUE_ADMIN_PANEL


@admin.register(Category)
class CategoriesAdmin(admin.ModelAdmin):
    """Админ панель для модели Категории."""

    list_display = ('pk', 'name', 'slug')
    list_editable = ('name',)
    list_filter = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    empty_value_display = EMPTY_VALUE_ADMIN_PANEL


@admin.register(Genre)
class GenresAdmin(admin.ModelAdmin):
    """Админ панель для модели Жанры."""

    list_display = ('pk', 'name', 'slug')
    list_editable = ('name',)
    list_filter = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    empty_value_display = EMPTY_VALUE_ADMIN_PANEL


@admin.register(Title)
class TitlesAdmin(admin.ModelAdmin):
    """Админ панель для модели Произведения."""

    list_display = ('pk', 'name', 'year', 'description', 'category')
    list_editable = ('name', 'year', 'description', 'category')
    list_filter = ('name', 'year', 'category')
    empty_value_display = EMPTY_VALUE_ADMIN_PANEL


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Админ панель для модели Ревью."""
    list_display = ('author', 'title', 'text', 'score', 'pub_date')
    search_fields = ('title',)
    list_filter = ('author', 'title')
    empty_value_display = EMPTY_VALUE_ADMIN_PANEL


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Админ панель для модели Комменты."""
    list_display = ('author', 'review', 'text', 'pub_date')
    search_fields = ('review',)
    list_filter = ('author', 'review')
    empty_value_display = EMPTY_VALUE_ADMIN_PANEL
