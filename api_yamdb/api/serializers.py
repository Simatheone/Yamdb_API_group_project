from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Category, Comment, CustomUser, Genre, Review, Title

from .utils import CurrentTitleDefault


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


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True,
        slug_field='username'
    )
    title = serializers.HiddenField(
        default=CurrentTitleDefault()
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')
        model = Review
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title')
            )
        ]

    def validate(self, data):
        if not 1 <= data['score'] <= 10:
            raise serializers.ValidationError(
                'Оценка может быть от 1 до 10!'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date',)
        model = Comment
