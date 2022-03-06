from rest_framework import permissions

from reviews.models import USER_ROLE_ADMIN, USER_ROLE_MODERATOR


class IsAdmin(permissions.BasePermission):
    """
    Кастомный пермишен для админа,суперюзреа.
    Только админ либо супер юзер имеют права.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role == USER_ROLE_ADMIN or request.user.is_superuser
        )


class IsOwnerAdminModeratorOrReadOnly(permissions.BasePermission):
    """
    Кастомный пермишен для админа,суперюзреа, модера, автора.
    Админ, модератор, автор, суперюзер имеют права на доступ.
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        roles = (USER_ROLE_MODERATOR, USER_ROLE_ADMIN)
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.role in roles
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Кастомный пермишен для админа,суперюзреа.
    Админ, суперюзер имеют права на доступ для записи.
    Остальные пользователи на чтение.
    """
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated
            and (request.user.is_superuser
                 or request.user.role == USER_ROLE_ADMIN)
        )
