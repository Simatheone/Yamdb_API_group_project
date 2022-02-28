from reviews.models import (
    Categories, Genres, Titles
)


class CategoriesSerializer:
    """Сериализатор для модели Категории."""

    class Meta:
        model = Categories
        fields = ()


class GenresSerializer:
    """Сериализатор для модели Жанры."""

    class Meta:
        model = Genres
        fields = ()


class TitlesSerializer:
    """Сериализатор для модели Произведения."""

    class Meta:
        model = Titles
        fields = ()
