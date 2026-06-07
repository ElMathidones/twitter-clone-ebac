from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase

from accounts.models import Follow
from .models import Comment, Like, Post


class PostViewTest(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(
            username='author',
            password='StrongPass123!'
        )
        self.user = User.objects.create_user(
            username='user',
            password='StrongPass123!'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='StrongPass123!'
        )

    def test_authenticated_user_can_create_post(self):
        self.client.login(username='author', password='StrongPass123!')

        response = self.client.post(reverse('post_create'), {
            'content': 'Minha primeira postagem.'
        })

        post = Post.objects.get(content='Minha primeira postagem.')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(post.author, self.author)

    def test_feed_shows_only_followed_users_posts(self):
        followed_post = Post.objects.create(
            author=self.author,
            content='Post de quem eu sigo.'
        )
        not_followed_post = Post.objects.create(
            author=self.other_user,
            content='Post de quem eu não sigo.'
        )

        Follow.objects.create(
            follower=self.user,
            following=self.author
        )

        self.client.login(username='user', password='StrongPass123!')

        response = self.client.get(reverse('feed'))

        self.assertContains(response, followed_post.content)
        self.assertNotContains(response, not_followed_post.content)

    def test_author_can_update_post(self):
        post = Post.objects.create(
            author=self.author,
            content='Texto antigo.'
        )

        self.client.login(username='author', password='StrongPass123!')

        response = self.client.post(reverse('post_update', args=[post.pk]), {
            'content': 'Texto atualizado.'
        })

        post.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(post.content, 'Texto atualizado.')

    def test_non_author_cannot_update_post(self):
        post = Post.objects.create(
            author=self.author,
            content='Texto original.'
        )

        self.client.login(username='user', password='StrongPass123!')

        response = self.client.post(reverse('post_update', args=[post.pk]), {
            'content': 'Tentativa inválida.'
        })

        post.refresh_from_db()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(post.content, 'Texto original.')

    def test_user_can_like_and_unlike_post(self):
        post = Post.objects.create(
            author=self.author,
            content='Post para curtir.'
        )

        self.client.login(username='user', password='StrongPass123!')

        like_url = reverse('post_like', args=[post.pk])

        response = self.client.post(like_url, {'next': reverse('feed')})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Like.objects.filter(user=self.user, post=post).exists()
        )

        response = self.client.post(like_url, {'next': reverse('feed')})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Like.objects.filter(user=self.user, post=post).exists()
        )

    def test_user_can_comment_on_post(self):
        post = Post.objects.create(
            author=self.author,
            content='Post para comentar.'
        )

        self.client.login(username='user', password='StrongPass123!')

        response = self.client.post(reverse('post_detail', args=[post.pk]), {
            'content': 'Comentário de teste.'
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Comment.objects.filter(
                user=self.user,
                post=post,
                content='Comentário de teste.'
            ).exists()
        )


class PostAPITest(APITestCase):
    def setUp(self):
        self.author = User.objects.create_user(
            username='api_author',
            password='StrongPass123!'
        )
        self.user = User.objects.create_user(
            username='api_user',
            password='StrongPass123!'
        )

        self.post = Post.objects.create(
            author=self.author,
            content='Post criado para teste de API.'
        )

        self.client.force_authenticate(user=self.user)

    def test_api_can_list_posts(self):
        response = self.client.get('/api/posts/')

        self.assertEqual(response.status_code, 200)

    def test_api_can_create_post(self):
        response = self.client.post('/api/posts/', {
            'content': 'Post criado pela API.'
        }, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            Post.objects.filter(
                author=self.user,
                content='Post criado pela API.'
            ).exists()
        )

    def test_api_feed_returns_followed_users_posts(self):
        Follow.objects.create(
            follower=self.user,
            following=self.author
        )

        response = self.client.get('/api/posts/feed/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['content'], self.post.content)

    def test_api_can_like_and_unlike_post(self):
        like_url = f'/api/posts/{self.post.pk}/like/'

        response = self.client.post(like_url)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            Like.objects.filter(user=self.user, post=self.post).exists()
        )

        response = self.client.post(like_url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            Like.objects.filter(user=self.user, post=self.post).exists()
        )

    def test_api_can_create_comment(self):
        response = self.client.post(
            f'/api/posts/{self.post.pk}/comments/',
            {'content': 'Comentário criado pela API.'},
            format='json'
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            Comment.objects.filter(
                user=self.user,
                post=self.post,
                content='Comentário criado pela API.'
            ).exists()
        )
