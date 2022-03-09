from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.db import models

from api_yamdb.settings import CINEMATOGRAPHY_CREATION_YEAR, MIN_STR

USER_ROLE_USER = 'user'
USER_ROLE_MODERATOR = 'moderator'
USER_ROLE_ADMIN = 'admin'

USER_ROLE_CHOICES = (
    (USER_ROLE_USER, 'Пользователь'),
    (USER_ROLE_MODERATOR, 'Модератор'),
    (USER_ROLE_ADMIN, 'Админ'),
)


def validate_year(value):
    """
    Валидатор для проверки введенного года выпуска произведения.
    """
    year_now = datetime.now().year
    if year_now >= value >= CINEMATOGRAPHY_CREATION_YEAR:
        return value
    else:
        raise ValidationError(
            f'Год выпуска произведения {value} не может быть больше '
            f'настоящего года {year_now}, либо меньше даты '
            f'создания кинематографа "{CINEMATOGRAPHY_CREATION_YEAR}"г.'
            'Проверьте введеные данные.'
        )


class CustomUser(AbstractUser):
    """Модель Кастомного Юзера."""

    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        verbose_name='Пользователь',
        max_length=257,
        unique=True,
        help_text='Введите username',
        validators=(username_validator,),
        error_messages={
            'unique': 'Пользователь с таким именем уже зарегистрирован',
        },
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=257,
        blank=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=257,
        blank=True
    )
    email = models.EmailField(
        max_length=257, unique=True, verbose_name='Электронная почта'
    )
    role = models.CharField(
        max_length=16,
        choices=USER_ROLE_CHOICES,
        default=USER_ROLE_USER,
        verbose_name='Роль',
    )
    bio = models.TextField('Биография', blank=True)
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=50,
        blank=True
    )

    class Meta:
        db_table = 'custom_user'
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=('username', 'email'), name='unique_username_email'
            )
        ]

    def __str__(self):
        return self.username


class Category(models.Model):
    """Модель Категории."""

    name = models.CharField(
        'Категория', max_length=256, help_text='Введите название категории'
    )
    slug = models.SlugField('Категория слаг', unique=True, max_length=50)

    class Meta:
        db_table = 'categories'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name[:MIN_STR]


class Genre(models.Model):
    """Модель Жанры."""

    name = models.CharField(
        'Жанр',
        max_length=256,
        help_text='Введите название жанра'
    )
    slug = models.SlugField('Жанр слаг', unique=True, max_length=50)

    class Meta:
        db_table = 'genres'
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name[:MIN_STR]


class Title(models.Model):
    """Модель Произведения."""

    name = models.CharField(
        'Название произведения',
        max_length=256,
        help_text='Введите название произведения',
    )
    year = models.IntegerField(
        'Год выпуска',
        validators=(validate_year,),
        help_text='Введите год выпуска произведения',
    )
    description = models.TextField(
        'Описание произведения',
        blank=True,
        help_text='Введите описание произведения',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
        blank=True,
        verbose_name='Категория произведения',
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        through='GenreTitle',
        verbose_name='Жанры произведения',
    )

    class Meta:
        db_table = 'titles'
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name', 'year')

    def __str__(self):
        return self.name[:MIN_STR]


class GenreTitle(models.Model):
    """
    Модель через которую реализована свзяь m2m.
    Связные модели: Titles, Genre.
    """

    genre = models.ForeignKey(
        Genre,
        related_name='genretitle',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    title = models.ForeignKey(
        Title,
        related_name='genretitle',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    class Meta:
        db_table = 'genre_title'

    def __str__(self):
        return f'{self.genre.name} {self.title.name}'


class Review(models.Model):
    """Модель Ревью."""

    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
    )
    text = models.TextField('Текст', help_text='Введите текст обзора')
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )
    score = models.PositiveIntegerField(
        verbose_name='Оценка', help_text='Оцените произведение'
    )
    pub_date = models.DateTimeField('Дата обзора', auto_now_add=True)

    class Meta:
        db_table = 'reviews'
        ordering = (
            '-pub_date',
            'author',
        )
        indexes = (
            models.Index(
                fields=('author',),
                name='author_post_idx'
            ),
            models.Index(
                fields=('text',),
                name='search_text_idx'
            ),
        )
        verbose_name = 'Обзор'
        verbose_name_plural = 'Обзоры'
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author'), name='unique_title'
            )
        ]

    def __str__(self):
        return self.text[:MIN_STR]


class Comment(models.Model):
    """Модель Комментарии."""

    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )
    text = models.TextField(
        'Текст комментария',
        help_text='Введите текст комментария'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Обзор'
    )
    pub_date = models.DateTimeField('Дата добавления', auto_now_add=True)

    class Meta:
        db_table = 'comments'
        ordering = (
            '-pub_date',
            'author',
        )
        indexes = (
            models.Index(
                fields=('review',),
                name='review_comment_idx'
            ),
        )
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:MIN_STR]
