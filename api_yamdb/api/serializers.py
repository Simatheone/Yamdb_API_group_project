from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from reviews.models import Category, CustomUser, Genre, Title


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
