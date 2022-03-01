from reviews.models import (
    Category, Genre, Title
)


class CategoriesSerializer:
    """Сериализатор для модели Категории."""

    class Meta:
        model = Category
        fields = ()


class GenresSerializer:
    """Сериализатор для модели Жанры."""

    class Meta:
        model = Genre
        fields = ()


class TitlesSerializer:
    """Сериализатор для модели Произведения."""

    class Meta:
        model = Title
        fields = ()
