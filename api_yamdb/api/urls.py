from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AccessTokenView, EmailRegistrationView, UserViewSet
from .views import (
    AccessTokenView, EmailRegistrationView, UserViewSet,
    CategoryViewSet, GenreViewSet, TitleViewSet
)

router_v1 = DefaultRouter()
router_v1.register(r'users', UserViewSet, basename='users')
router_v1.register(r'categories', CategoryViewSet, basename='categories')
router_v1.register(r'genres', GenreViewSet, basename='genres')
router_v1.register(r'titles', TitleViewSet, basename='titles')

urlpatterns = [
    path("v1/", include(router_v1.urls)),
    path("v1/auth/signup/", EmailRegistrationView.as_view()),
    path("v1/auth/token/", AccessTokenView.as_view()),
]
