from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

USER_ROLE_USER = 'user'
USER_ROLE_MODERATOR = 'moderator'
USER_ROLE_ADMIN = 'admin'

USER_ROLE_CHOICES = (
    (USER_ROLE_USER, 'Пользователь'),
    (USER_ROLE_MODERATOR, 'Модератор'),
    (USER_ROLE_ADMIN, 'Админ'),
)


class CustomUser(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        verbose_name='Пользователь',
        max_length=257,
        unique=True,
        help_text=(
            'Представьтесь пожалуйста.'
        ),
        validators=[username_validator],
        error_messages={
            'unique': 'Пользователь с таким именем уже зарегистрирован',
        },
    )
    first_name = models.CharField(
        verbose_name='Имя', max_length=257, blank=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия', max_length=257, blank=True
    )
    email = models.EmailField(
        max_length=257,
        unique=True,
        verbose_name='Электронная почта'
    )
    role = models.CharField(
        max_length=16,
        choices=USER_ROLE_CHOICES,
        default=USER_ROLE_USER,
        verbose_name='Роль'
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография'
    )
    confirmation_code = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Код для авторизации'
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email'
            )
        ]

    def is_admin(self):
        return self.is_staff or self.role == USER_ROLE_ADMIN

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
