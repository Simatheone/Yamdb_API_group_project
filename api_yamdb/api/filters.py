from django_filters import CharFilter, FilterSet

from reviews.models import Title


class TitleFilterBackend(FilterSet):
    """
    Кастомный фильтр для Title.
    Добавляет возможность поиска по полю slug жанра и категории.
    """

    genre = CharFilter(field_name='genre__slug', lookup_expr='icontains')
    category = CharFilter(field_name='category__slug', lookup_expr='icontains')
    name = CharFilter(field_name='name', lookup_expr='contains')

    class Meta:
        model = Title
        fields = ('genre', 'category', 'name', 'year')
