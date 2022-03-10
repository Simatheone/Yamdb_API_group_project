from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api_yamdb.settings import EMAIL_HOST_USER
from reviews.models import Category, CustomUser, Genre, Title

from .filters import TitleFilterBackend
from .pagination import CategoryPagination
from .permissions import (IsAdmin, IsAdminOrReadOnly,
                          IsOwnerAdminModeratorOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          ConfirmationCodeSerializer, EmailSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleReadSerializer, TitleWriteSerializer,
                          UserSerializer)


class ListCreateDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """
    Кастомный вьюсет для наследования.
    Вьюсеты использующие наслодование: GenreViewSet, CategoryViewSet
    """
    pass


class UserViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для кастомного юзера.
    Обрабатываемые запросы: GET, POST, PATCH, DELETE.
    Эндпоинты: /users/me/
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        detail=False,
        methods=('get', 'patch'),
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(data=serializer.data)
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(data=serializer.data)


class EmailRegistrationView(views.APIView):
    """
    Вьюсет отправки регестрации юзера.
    Обрабатываемые запросы: POST.
    Эндпоинты: /auth/signup/
    """
    permission_classes = (AllowAny,)

    @staticmethod
    def mail_send(email, user):
        send_mail(
            subject='YaMDB Confirmation Code',
            message=(
                f"""
                Hello!

                Your confirmation: {user.confirmation_code}
            """
            ),
            from_email=EMAIL_HOST_USER,
            recipient_list=(email,),
            fail_silently=False,
        )

    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data['email']
            username = serializer.validated_data['username']
            serializer.save()
            user = get_object_or_404(CustomUser, username=username)
            self.mail_send(email, user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccessTokenView(views.APIView):
    """
    Вьюсет для получения/обновления токена.
    Обрабатываемые запросы: POST.
    Эндпоинты: /auth/token/
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = ConfirmationCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = serializer.validated_data['confirmation_code']
        username = serializer.validated_data['username']
        try:
            user = get_object_or_404(CustomUser, username=username)
        except CustomUser.DoesNotExist:
            return Response(
                {'email': 'Not found'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if user.confirmation_code != confirmation_code:
            return Response(
                {
                    'confirmation_code': (
                        'Invalid confirmation' f'code for email {user.email}'
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(self.get_token(user), status=status.HTTP_200_OK)

    @staticmethod
    def get_token(user):
        return {'token': str(AccessToken.for_user(user))}


class CategoryViewSet(ListCreateDestroyViewSet):
    """
    Вьюсет для модели Category.
    Обрабатывает запросы: GET, POST, DELETE
    Эндпоинты: /categories/, /categories/{slug}/
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'
    pagination_class = CategoryPagination


class GenreViewSet(ListCreateDestroyViewSet):
    """
    Вьюсет для модели Genre.
    Обрабатывает запросы: GET, POST, DELETE
    Эндпоинты: /genres/, /genres/{slug}/
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'
    pagination_class = PageNumberPagination

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class TitleViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для модели Title.
    Обрабатывает запросы: GET, POST, PATCH, DELETE, GET 1 элемента.
    Эндпоинты: /titles/, /titles/{titles_id}/
    """
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilterBackend
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return TitleWriteSerializer
        return TitleReadSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для модели Review.
    Обрабатывает запросы: GET, POST, PATCH, DELETE, GET 1 элемента.
    Эндпоинты: /titles/{title_id}/reviews/,
    /titles/{title_id}/reviews/{review_id}
    """
    serializer_class = ReviewSerializer
    permission_classes = (IsOwnerAdminModeratorOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('=author__username',)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для модели Comment.
    Обрабатывает запросы: GET, POST, PATCH, DELETE, GET 1 элемента.
    Эндпоинты: /titles/{title_id}/reviews/{review_id}/comments,
    /titles/{title_id}/reviews/{review_id}
    """
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerAdminModeratorOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        review_id = self.kwargs.get('review_id')
        review = title.reviews.get(pk=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        review_id = self.kwargs.get('review_id')
        review = title.reviews.get(pk=review_id)
        serializer.save(author=self.request.user, review=review)
