from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (get_jwt_token, signup, CategoryViewSet, CommentViewSet,
                    GenreViewSet, ReviewViewSet, TitleViewSet, UserViewSet)

V1 = 'v1/'

router_v1 = DefaultRouter()
router_v1.register(V1 + r'users', UserViewSet, basename='users')
router_v1.register(V1 + r'categories', CategoryViewSet, basename='categories')
router_v1.register(V1 + r'genres', GenreViewSet, basename='genres')
router_v1.register(V1 + 'titles', TitleViewSet, basename='titles')
router_v1.register(
    V1 + r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews')
router_v1.register(
    V1 + r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')

urlpatterns = [
    path(f'{V1}auth/signup/', signup, name='signup'),
    path(f'{V1}auth/token/', get_jwt_token, name='get_jwt_token'),
    path('', include(router_v1.urls)),
]
