from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Follow, Profile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Profile
        fields = [
            'id',
            'username',
            'email',
            'display_name',
            'bio',
            'avatar',
        ]


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    followers_count = serializers.IntegerField(source='followers.count', read_only=True)
    following_count = serializers.IntegerField(source='following.count', read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'profile',
            'followers_count',
            'following_count',
        ]


class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.StringRelatedField(read_only=True)
    following = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Follow
        fields = [
            'id',
            'follower',
            'following',
            'created_at',
        ]
