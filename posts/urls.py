from django.urls import path

from . import views


urlpatterns = [
    path('', views.feed_view, name='feed'),
    path('posts/create/', views.create_post_view, name='post_create'),
    path('posts/<int:pk>/', views.post_detail_view, name='post_detail'),
    path('posts/<int:pk>/like/', views.like_toggle_view, name='post_like'),
    path('posts/<int:pk>/edit/', views.update_post_view, name='post_update'),
    path('posts/<int:pk>/delete/', views.delete_post_view, name='post_delete'),
]
