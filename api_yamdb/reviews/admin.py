from django.contrib import admin

from .models import Comment, Title, Category, Genre, User, Review


EMPTY_VALUE = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Represents the model Comment in admin interface."""
    list_display = ('id', 'text', 'author', 'review')
    empty_value_display = EMPTY_VALUE

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Represents the model Category in admin interface."""
    list_display = ('id', 'name', 'slug')
    empty_value_display = EMPTY_VALUE


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Represents the model Title in admin interface."""
    list_display = ('id', 'name', 'year', 'category', 'get_genres')

    def get_genres(self, obj):
        return '\n'.join([str(p) for p in obj.genre.all()])



@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Represents the model Review in admin interface."""
    list_display = ('id', 'text', 'score', 'author', 'title')
    empty_value_display = EMPTY_VALUE


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Represents the model User in admin interface."""
    list_display = ('id', 'username', 'email', 'password')
    empty_value_display = EMPTY_VALUE


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Represents the model Comment in admin interface."""
    list_display = ('id', 'name')
    empty_value_display = EMPTY_VALUE
