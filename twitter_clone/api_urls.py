from django.urls import include, path
from rest_framework.routers import DefaultRouter

from accounts.api_views import UserViewSet
from posts.api_views import CommentViewSet, PostViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('posts', PostViewSet, basename='posts')
router.register('comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('', include(router.urls)),
]
