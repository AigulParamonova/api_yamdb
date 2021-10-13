from rest_framework import serializers, validators
from reviews.models import Category, Comment, Genre, Review, Title, User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email',
                    'bio', 'role')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
