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
        raise ValidationError(f"Имя пользователя: {username} недоступно")
    return username


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("username", "email")
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


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Произведения."""
    rating = serializers.SerializerMethodField(read_only=True)
    genre = GenreSerializer(many=True)
    category = CategorySerializer(many=False)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )

    def get_rating(self, obj):
        """Метод для вычисления усреднённой оценки произведения."""
        reviews = Review.objects.filter(title=obj.id)
        total_scores = []
        for review in reviews:
            total_scores.append(review.score)
        if not total_scores:
            return None
        rating = round(sum(total_scores) / len(total_scores))
        return rating


class TitlesRepresentation(serializers.SlugRelatedField):

    def to_representation(self, value):
        return {
            'name': value.name,
            'slug': value.slug
        }


class TitleWriteSerializer(serializers.ModelSerializer):

    genre = TitlesRepresentation(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = TitlesRepresentation(
        slug_field='slug',
        queryset=Category.objects.all(),
        many=False
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')


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
        default=serializers.CurrentUserDefault(),
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'review', 'pub_date',)
        read_only_fields = ('id', 'pub_date', 'review')
        model = Comment
