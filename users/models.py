import secrets
import string

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.db import models

ME_NOT_ALLOWED_MSG = 'Вы не можете использовать {value} в качестве username!'


def validate_not_me(value):
    if value == 'me':
        raise ValidationError(ME_NOT_ALLOWED_MSG.format(value=value))
    return value


ROLE_CHOICES = (
    ('admin', 'admin'),
    ('moderator', 'moderator'),
    ('user', 'user'),
)


def create_token():
    alphabet = string.ascii_letters.upper() + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(20))


class CustomUserManager(BaseUserManager):

    def create_user(self, username, email, password=None, **kwargs):
        user = self.model(username=username, email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password, **kwargs):
        user = self.model(
            username=username,
            email=email,
            is_staff=True,
            is_superuser=True,
            **kwargs
        )
        user.set_password(password)
        user.save()
        return user


class User(AbstractUser):
    username = models.CharField(
        'Ник',
        unique=True,
        max_length=150,
        validators=(validate_not_me,)
    )
    email = models.EmailField('e-mail', unique=True)
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Пользовательская роль',
        max_length=50,
        choices=ROLE_CHOICES,
        default='user'
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=20,
        default=create_token
    )
    REQUIRED_FIELDS = ('email',)

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    objects = CustomUserManager()
