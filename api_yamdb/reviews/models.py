from django.db import models

"""
Второй разработчик пишет категории (Categories),
жанры (Genres) и произведения (Titles):
модели, представления и эндпойнты для них.
"""


class Categories(models.Moodel):
    """Модель Категории."""

    """
    При удалении объекта категории Category не нужно
    удалять связанные с этой категорией произведения.
    """
    # id, name, slug
    name = models.CharField('Категория', max_length=256)
    slug = models.SlugField('Категория слаг', unique=True, max_length=50)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Genres(models.Model):
    """Модель Жанры."""

    """
    При удалении объекта жанра Genre не нужно
    удалять связанные с этим жанром произведения.
    """
    # id, name, slug
    name = models.CharField('Жанр', max_length=256)
    slug = models.SlugField('Жанр слаг', unique=True, max_length=50)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Titles(models.Model):
    """Модель Произведения."""
    """
    При удалении объекта произведения Title должны удаляться
    все отзывы к этому произведению и комментарии к ним.
    """
    # id, name, year, category
    name = models.CharField('Название произведения', max_length=256)
    year = models.IntegerField('Год выпуска', max_length=4)
    description = models.TextField('Описание произведения', blank=True)
    category = models.ForeignKey('Categories', on_delete=models.SET_NULL,
                                 related_name='categories', blank=True,
                                 verbose_name='Категория произведения')
    genre = models.ManyToManyField('Genres', related_name='genres',
                                   through='GenreTitle')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:30]


class GenreTitle(models.Model):
    """
    Модель через которую реализована свзяь m2m.
    Связанные модели: Titles, Genre.
    """
    # Метод удаления полей ???
    genre = models.ForeignKey(Genres, on_delete=models.SET_NULL, blank=True,
                              null=True)
    title = models.ForeignKey(Titles, on_delete=models.CASCADE)
