from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    display_name = models.CharField(
        max_length=100,
        blank=True
    )
    bio = models.TextField(
        blank=True
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.display_name or self.user.username


class Follow(models.Model):
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f'{self.follower.username} follows {self.following.username}'
