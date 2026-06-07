from django.contrib.auth.models import User
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Follow
from .serializers import FollowSerializer, UserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.select_related('profile').all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        user_to_follow = self.get_object()

        if user_to_follow == request.user:
            return Response(
                {'detail': 'Você não pode seguir a si mesmo.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        follow, created = Follow.objects.get_or_create(
            follower=request.user,
            following=user_to_follow
        )

        if created:
            return Response(
                {'detail': 'Usuário seguido com sucesso.'},
                status=status.HTTP_201_CREATED
            )

        follow.delete()

        return Response(
            {'detail': 'Você deixou de seguir este usuário.'},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['get'])
    def followers(self, request, pk=None):
        user = self.get_object()
        followers = Follow.objects.filter(following=user)
        serializer = FollowSerializer(followers, many=True)

        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def following(self, request, pk=None):
        user = self.get_object()
        following = Follow.objects.filter(follower=user)
        serializer = FollowSerializer(following, many=True)

        return Response(serializer.data)
