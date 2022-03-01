from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from datetime import datetime

USER_ROLE_USER = "user"
USER_ROLE_MODERATOR = "moderator"
USER_ROLE_ADMIN = "admin"

USER_ROLE_CHOICES = (
    (USER_ROLE_USER, "Пользователь"),
    (USER_ROLE_MODERATOR, "Модератор"),
    (USER_ROLE_ADMIN, "Админ"),
)

User = get_user_model()


def validate_year(value):
    """
    Валидатор для проверки введенного года выпуска произведения.
    """
    year_now = datetime.now().year
    if year_now > value:
        return value
    else:
        raise ValidationError(
            f'Год выпуска произведения {value} не может быть больше '
            f'настоящего года {year_now}.'
        )


class CustomUser(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        verbose_name="Пользователь",
        max_length=257,
        unique=True,
        help_text=("Представьтесь пожалуйста."),
        validators=[username_validator],
        error_messages={
            "unique": "Пользователь с таким именем уже зарегистрирован",
        },
    )
    first_name = models.CharField(
        verbose_name="Имя", max_length=257, blank=True
    )
    last_name = models.CharField(
        verbose_name="Фамилия", max_length=257, blank=True
    )
    email = models.EmailField(
        max_length=257, unique=True, verbose_name="Электронная почта"
    )
    role = models.CharField(
        max_length=16,
        choices=USER_ROLE_CHOICES,
        default=USER_ROLE_USER,
        verbose_name="Роль",
    )
    bio = models.TextField(blank=True, verbose_name="Биография")
    confirmation_code = models.CharField(
        max_length=50, blank=True, verbose_name="Код для авторизации"
    )

    class Meta:
        ordering = ("username",)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        constraints = [
            models.UniqueConstraint(
                fields=["username", "email"], name="unique_username_email"
            )
        ]

    def is_admin(self):
        return self.is_staff or self.role == USER_ROLE_ADMIN


class Category(models.Model):
    """Модель Категории."""
    name = models.CharField('Категория', max_length=256)
    slug = models.SlugField('Категория слаг', unique=True, max_length=50)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name[:30]


class Genre(models.Model):
    """Модель Жанры."""
    name = models.CharField('Жанр', max_length=256)
    slug = models.SlugField('Жанр слаг', unique=True, max_length=50)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name[:30]


class Title(models.Model):
    """Модель Произведения."""

    name = models.CharField("Название произведения", max_length=256)
    year = models.IntegerField(
        "Год выпуска", validators=[validate_year]
    )
    description = models.TextField("Описание произведения", blank=True)
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        related_name="categories",
        blank=True,
        null=True,
        verbose_name="Категория произведения",
    )
    genre = models.ManyToManyField(
        "Genre", related_name="genres", through="GenreTitle"
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:30]


class GenreTitle(models.Model):
    """
    Модель через которую реализована свзяь m2m.
    Связные модели: Titles, Genre.
    """
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, blank=True,
                              null=True)
    title = models.ForeignKey(Title, on_delete=models.SET_NULL, blank=True,
                              null=True)


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    text = models.TextField(
        'Текст',
        help_text='Введите текст обзора'
    )
    title_id = models.ForeignKey(
        'Titles',
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    score = models.PositiveIntegerField(
        on_delete=models.CASCADE,
        verbose_name='Оценка',
        help_text='Оцените произведение'
    )
    pub_date = models.DateTimeField(
        'Дата обзора',
        auto_now_add=True
    )

    class Meta:
        db_table = 'reviews'
        ordering = ('-pub_date', 'author',)
        indexes = (
            models.Index(fields=['author'], name='author_post_idx'),
            models.Index(fields=['text'], name='search_text_idx'),
        )
        verbose_name = 'Обзор'
        verbose_name_plural = 'Обзоры'

    def __str__(self):
        return self.text[:30]


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    text = models.TextField(
        'Текст комментария',
        help_text='Введите текст комментария'
    )
    review_id = models.ForeignKey(
        'Review',
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Обзор'
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True
    )

    class Meta:
        db_table = 'comments'
        ordering = ('-pub_date', 'author',)
        indexes = (
            models.Index(
                fields=['review_id'],
                name='review_comment_idx'
            ),
        )
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:30]
