import django_filters

from django.conf import settings
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, status, permissions
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.exceptions import ParseError

from reviews.models import Category, Genre, Review, Title, User
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, GetTokenSerializer, UserSerializer,
                          ReviewSerializer, SignupSerializer, TitleSerializer,)
from .permissions import (IsAdmin, IsAdminOrReadOnly,
                          IsAuthorModeratorAdminOrReadOnly)
from .mixins import CustomViewSet


MAIL_SUBJECT = 'Регистрация на Yamdb.ru'
MESSAGE = 'Ваш код подтверждения: {confirmation_code}'
MAIL = settings.MAIL


@api_view(['POST'])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        email = request.data['email']
        username = request.data['username']
        if username == 'me':
            return Response(status=status.HTTP_400_BAD_REQUEST)
        username_exists = User.objects.filter(username=username).exists()
        email_exists = User.objects.filter(email=email).exists()
        if username_exists or email_exists:
            user_exists = User.objects.filter(
                username=username,
                email=email
            ).exists()
            if user_exists:
                user = User.objects.get(username=username, email=email)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            user = User.objects.create(username=username, email=email)
        confirmation_code = user.confirmation_code
        message = MESSAGE.format(confirmation_code=confirmation_code)
        send_mail(MAIL_SUBJECT, message, MAIL, [email])
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_jwt_token(request):
    serializer = GetTokenSerializer(data=request.data)
    if serializer.is_valid():
        username = request.data['username']
        confirmation_code = request.data['confirmation_code']
        user = get_object_or_404(User, username=username)
        if confirmation_code == user.confirmation_code:
            token = AccessToken.for_user(user)
            return Response({'token': f'{token}'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdmin, ]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('=username',)
    ordering_fields = ('username',)

    @action(methods=['patch', 'get'], detail=False,
            permission_classes=[permissions.IsAuthenticated],
            url_path='me', url_name='me')
    def me(self, request):
        user = self.request.user
        serializer = self.get_serializer(user)
        if self.request.method == 'PATCH':
            request.data._mutable = True
            data = request.data
            if data.get('role'):
                data.pop('role')
            if data.get('email'):
                new_email = data['email']
                if user.email != new_email:
                    if User.objects.filter(email=new_email).exists():
                        return Response(status=status.HTTP_400_BAD_REQUEST)
            if data.get('username'):
                new_name = data['username']
                if user.username != new_name:
                    if User.objects.filter(username=new_name).exists():
                        return Response(status=status.HTTP_400_BAD_REQUEST)
            serializer = self.get_serializer(
                user, data, partial=True)
            serializer.is_valid()
            serializer.save()
        return Response(serializer.data)


class CategoryViewSet(CustomViewSet):
    permission_classes = [IsAdminOrReadOnly, ]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name', )


class GenreViewSet(CustomViewSet):
    permission_classes = [IsAdminOrReadOnly, ]
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ('=name', )


class TitleFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='contains'
    )
    category = django_filters.CharFilter(
        field_name='category__slug',
        lookup_expr='exact'
    )
    genre = django_filters.CharFilter(
        field_name='genre__slug',
        lookup_expr='exact'
    )

    class Meta:
        model = Title
        fields = ['name', 'category', 'genre', 'year']


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    permission_classes = [IsAdminOrReadOnly, ]
    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if title.reviews.filter(author=self.request.user).exists():
            raise ParseError
        serializer.save(author=self.request.user, title=title)

    def perform_update(self, serializer):
        serializer.save()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        title_id = self.kwargs.get('title_id')
        review = get_object_or_404(Review, pk=review_id, title__id=title_id)
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)
