from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import Follow
from .models import Comment, Like, Post
from .permissions import IsOwnerOrAuthorOrReadOnly
from .serializers import CommentSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsOwnerOrAuthorOrReadOnly()]

        return [IsAuthenticated()]

    def get_queryset(self):
        return Post.objects.select_related(
            'author',
            'author__profile'
        ).prefetch_related(
            'likes',
            'comments'
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False, methods=['get'])
    def feed(self, request):
        followed_users = Follow.objects.filter(
            follower=request.user
        ).values_list('following', flat=True)

        posts = self.get_queryset().filter(author_id__in=followed_users)
        serializer = self.get_serializer(posts, many=True)

        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = self.get_object()

        like, created = Like.objects.get_or_create(
            user=request.user,
            post=post
        )

        if created:
            return Response(
                {'detail': 'Postagem curtida com sucesso.'},
                status=status.HTTP_201_CREATED
            )

        like.delete()

        return Response(
            {'detail': 'Curtida removida com sucesso.'},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['get', 'post'])
    def comments(self, request, pk=None):
        post = self.get_object()

        if request.method == 'GET':
            comments = post.comments.select_related('user', 'user__profile')
            serializer = CommentSerializer(comments, many=True)

            return Response(serializer.data)

        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user, post=post)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsOwnerOrAuthorOrReadOnly()]

        return [IsAuthenticated()]

    def get_queryset(self):
        return Comment.objects.select_related(
            'user',
            'user__profile',
            'post'
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
