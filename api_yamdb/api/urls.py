from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import AccessTokenView, EmailRegistrationView, UserViewSet

router_v1 = SimpleRouter()
router_v1.register("users", UserViewSet)

urlpatterns = [
    path("v1/", include(router_v1.urls)),
    path("v1/auth/signup/", EmailRegistrationView.as_view()),
    path("v1/auth/token/", AccessTokenView.as_view()),
]
