# from rest_framework import filters
from rest_framework import viewsets

from api.serializers import (
    CategoriesSerializer, GenresSerializer,
    TitlesSerializer
)
from reviews.models import (
    Categories, Genres, Titles
)


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
