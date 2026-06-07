from rest_framework import serializers

from .models import Comment, Like, Post


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'user',
            'post',
            'content',
            'created_at',
        ]
        read_only_fields = [
            'id',
            'user',
            'post',
            'created_at',
        ]


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'content',
            'created_at',
            'updated_at',
            'likes_count',
            'comments_count',
        ]
        read_only_fields = [
            'id',
            'author',
            'created_at',
            'updated_at',
            'likes_count',
            'comments_count',
        ]


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Like
        fields = [
            'id',
            'user',
            'post',
            'created_at',
        ]
        read_only_fields = [
            'id',
            'user',
            'created_at',
        ]
