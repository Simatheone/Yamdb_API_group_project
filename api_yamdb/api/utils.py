import uuid

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from api_yamdb.settings import EMAIL_HOST_USER
from reviews.models import CustomUser, Title


class CurrentTitleDefault:
    requires_context = True

    def __call__(self, serializer_field):
        title_id = serializer_field.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title

    def __repr__(self):
        return f'{self.__class__.__name__}'


def generate_and_send_confirmation_code_to_email(username):
    user = get_object_or_404(CustomUser, username=username)
    confirmation_code = str(uuid.uuid3(uuid.NAMESPACE_DNS, username))
    user.confirmation_code = confirmation_code
    send_mail(
        'Код подтвержения для завершения регистрации',
        f'Ваш код для получения JWT токена {user.confirmation_code}',
        EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )
    user.save()
