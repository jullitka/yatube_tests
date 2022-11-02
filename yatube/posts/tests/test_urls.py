from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from posts.models import Group, Post

User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.auth = User.objects.create_user(username='author')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.auth,
            text='Тестовый пост',
        )

    def setUp(self):
        self.authorized_author = Client()
        self.authorized_author.force_login(PostURLTests.auth)
        self.user = User.objects.create_user(username='NoName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_page_exists_at_desired_location(self):
        """Страница доступна любому пользователю."""
        url_names = (
            '/', '/group/Тестовый слаг/',
            '/profile/author/', f'/posts/{PostURLTests.post.id}/'
        )
        for address in url_names:
            with self.subTest(address=address):
                response = self.client.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create_exists_at_desired_location(self):
        """Страница доступна  любому авторизованному пользователю."""
        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create_exists_at_desired_location(self):
        """Страница /posts/<post_id>/edit/ доступна  автору."""
        response = self.authorized_author.get(
            f'/posts/{PostURLTests.post.id}/edit/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_page_url_redirect_anonymous(self):
        """Страница /create/, /posts/<post_id>/edit/ перенаправляет
        анонимного пользователя на страницу авторизации."""
        url_names = {
            '/create/': '/auth/login/?next=/create/',
            f'/posts/{PostURLTests.post.id}/edit/':
            f'/auth/login/?next=/posts/{PostURLTests.post.id}/edit/'
        }
        for address, log in url_names.items():
            with self.subTest(address=address):
                response = self.client.get(address, follow=True)
                self.assertRedirects(response, log)

    def test_edit_redirect_no_author(self):
        """Страница /posts/<post_id>/edit/ перенаправляет НЕ автора"""
        response = self.authorized_client.get(
            f'/posts/{PostURLTests.post.id}/edit/')
        self.assertRedirects(response, f'/posts/{PostURLTests.post.id}/')

    def test_unexisting_page_at_desired_location(self):
        """Страница /unexisting_page/ вернет ошибку 404."""
        response = self.authorized_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            '/': 'posts/index.html',
            '/group/Тестовый слаг/': 'posts/group_list.html',
            '/profile/author/': 'posts/profile.html',
            f'/posts/{PostURLTests.post.id}/': 'posts/post_detail.html',
            '/create/': 'posts/create_post.html',
            f'/posts/{PostURLTests.post.id}/edit/': 'posts/create_post.html'
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_author.get(address)
                self.assertTemplateUsed(response, template)
