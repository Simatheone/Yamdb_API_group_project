from rest_framework.pagination import PageNumberPagination


class CategoryPagination(PageNumberPagination):
    """Кастомный пагинатор для Category."""

    page_size = 10
