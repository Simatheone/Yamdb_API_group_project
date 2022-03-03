from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from reviews.models import (
    Category, CustomUser, Genre, Title,
    Review
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            "email",
            "username",
            "bio",
            "role",
            "first_name",
            "last_name",
        ]
        model = CustomUser
        extra_kwargs = {
            "email": {"required": True},
            "username": {"required": True},
        }


def validate_username(username):
    if username == "me":
        raise ValidationError(f"Имя пользователя: {username} недоступено")
    return username


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["username", "email"]
        model = CustomUser
        extra_kwargs = {
            "email": {"required": True},
            "username": {"required": True},
        }


class ConfirmationCodeSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


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
    genre = GenreSerializer(many=True)

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
