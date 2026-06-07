from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Follow


class AccountModelTest(TestCase):
    def test_profile_is_created_when_user_is_created(self):
        user = User.objects.create_user(
            username='mathias',
            password='StrongPass123!'
        )

        self.assertTrue(hasattr(user, 'profile'))
        self.assertEqual(user.profile.display_name, 'mathias')

    def test_user_can_follow_another_user(self):
        follower = User.objects.create_user(
            username='follower',
            password='StrongPass123!'
        )
        following = User.objects.create_user(
            username='following',
            password='StrongPass123!'
        )

        Follow.objects.create(
            follower=follower,
            following=following
        )

        self.assertEqual(follower.following.count(), 1)
        self.assertEqual(following.followers.count(), 1)


class AccountViewTest(TestCase):
    def test_signup_view_creates_user(self):
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'email': 'newuser@email.com',
            'display_name': 'New User',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })

        user = User.objects.get(username='newuser')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(user.email, 'newuser@email.com')
        self.assertEqual(user.profile.display_name, 'New User')

    def test_authenticated_user_can_follow_and_unfollow(self):
        user = User.objects.create_user(
            username='user',
            password='StrongPass123!'
        )
        other_user = User.objects.create_user(
            username='otheruser',
            password='StrongPass123!'
        )

        self.client.login(username='user', password='StrongPass123!')

        follow_url = reverse('follow_toggle', args=[other_user.username])

        response = self.client.post(follow_url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Follow.objects.filter(
                follower=user,
                following=other_user
            ).exists()
        )

        response = self.client.post(follow_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Follow.objects.filter(
                follower=user,
                following=other_user
            ).exists()
        )
