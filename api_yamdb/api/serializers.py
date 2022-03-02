from rest_framework import serializers

from reviews.models import (
    Category, Genre, Review, Title
)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Категории."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Жанры."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Произведения."""
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        read_only = ('id', 'description')

    def get_ratings(self, obj):
        """Метод для вычисления усреднённой оценки произведения."""
        score = Review.objects.filter(score__reviews=obj.id)
        rating = sum(score) / len(score)
        return rating
