from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    CategoriesViewSet, GenresViewSet, TitlesViewSet
)

router_v1 = DefaultRouter()
router_v1.register(r'categories', CategoriesViewSet)
router_v1.register(r'genres', GenresViewSet)
router_v1.register(r'titles', TitlesViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
