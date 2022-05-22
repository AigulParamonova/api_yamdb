from django.contrib import admin

from .models import User


EMPTY_VALUE = '-пусто-'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Represents the model User in admin interface."""
    list_display = ('id', 'username', 'email', 'password')
    empty_value_display = EMPTY_VALUE
