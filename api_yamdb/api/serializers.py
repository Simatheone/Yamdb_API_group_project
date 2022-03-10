from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Comment, CustomUser, Genre, Review, Title

from .utils import CurrentTitleDefault


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Кастом Юзер."""

    class Meta:
        fields = [
            'email',
            'username',
            'bio',
            'role',
            'first_name',
            'last_name',
        ]
        model = CustomUser
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
        }


class EmailSerializer(serializers.ModelSerializer):
    """Сериализатор для отправки кода подтверждения на email."""

    class Meta:
        fields = ('username', 'email')
        model = CustomUser
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
        }

    def validate_username(self, value):
        if value == 'me':
            raise ValidationError(f'Имя пользователя: {value} недоступно')
        return value


class ConfirmationCodeSerializer(serializers.Serializer):
    """Сериализатор для кода подтверждения."""

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
    """Сериализатор для чтения Произведения."""

    rating = serializers.SerializerMethodField(read_only=True)
    genre = GenreSerializer(many=True)
    category = CategorySerializer(many=False)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')

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
    """Метод отображения Произведения."""
    def to_representation(self, value):
        return {'name': value.name, 'slug': value.slug}


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для записи Произведений."""

    genre = TitlesRepresentation(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )
    category = TitlesRepresentation(
        slug_field='slug', queryset=Category.objects.all(), many=False
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Ревью."""

    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True,
        slug_field='username'
    )
    title = serializers.HiddenField(default=CurrentTitleDefault())

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')
        model = Review
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(), fields=('author', 'title')
            )
        ]

    def validate_score(self, value):
        """
        Валидатор для проверки поля score.
        Проверяет, что введеное число находится в интвервале
        от 1 до 10.
        """
        if not 1 <= value <= 10:
            raise serializers.ValidationError('Оценка может быть от 1 до 10!')
        return value

    def validate_title(self, value):
        """
        Валидатор для проверки оставленного отзыва.
        Проверят, оставлял ли юзер отзыв о данном произведении.
        В случае повторного отзыва вызывает ошибка.
        """
        username = self.context.get('request').user
        reviews = Review.objects.filter(author=username, title=value).exists()
        if reviews:
            raise serializers.ValidationError(
                'Нельзя добавить второй отзыв на то же самое произведение!'
            )
        return value


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Комментарий."""

    author = serializers.SlugRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault(),
        slug_field='username'
    )

    class Meta:
        fields = (
            'id',
            'text',
            'author',
            'review',
            'pub_date',
        )
        read_only_fields = ('id', 'pub_date', 'review')
        model = Comment
