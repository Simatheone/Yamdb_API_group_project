# from rest_framework import filters
from rest_framework import viewsets

from .serializers import (
    CategoriesSerializer, GenresSerializer,
    TitlesSerializer
)
from reviews.models import (
    Category, Genre, Title
)


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitlesSerializer
