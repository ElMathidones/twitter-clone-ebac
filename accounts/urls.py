from django.urls import path

from . import views


urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('profile/<str:username>/follow/', views.follow_toggle_view, name='follow_toggle'),
]
