# from rest_framework import filters
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination

from .pagination import CategoryPagination
from .serializers import (
    CategorySerializer, GenreSerializer,
    TitleSerializer
)
from reviews.models import (
    Category, Genre, Title
)


class GetCreateDeleteViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                             mixins.DestroyModelMixin, viewsets.GenericViewSet
                             ):
    pass


class CategoryViewSet(GetCreateDeleteViewSet):
    """
    Вьюсет для модели Category.
    Обрабатывает запросы: GET, POST, DELETE
    Эндпоинты: /categories/, /categories/{slug}/
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = None
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    pagination_class = CategoryPagination

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class GenreViewSet(GetCreateDeleteViewSet):
    """
    Вьюсет для модели Genre.
    Обрабатывает запросы: GET, POST, DELETE
    Эндпоинты: /genres/, /genres/{slug}/
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = None
    pagination_class = PageNumberPagination


class TitleViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для модели Title.
    Обрабатывает запросы: GET, POST, PATCH, DELETE, GET 1 элемента.
    Эндпоинты: /titles/, /titles/{titles_id}/
    """
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = None
    pagination_class = PageNumberPagination

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
