from django import forms
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post

User = get_user_model()


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.auth = User.objects.create_user(username='author')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.group_2 = Group.objects.create(
            title='Новая тестовая группа',
            slug='Тестовый слаг новой группы',
            description='Тестовое описание новой группы'
        )
        cls.post = Post.objects.create(
            author=cls.auth,
            text='Тестовый пост',
            group=cls.group
        )
        cls.templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse(
                'posts:group_list',
                kwargs={'slug': cls.group.slug}
            ): 'posts/group_list.html',
            reverse(
                'posts:post_detail',
                kwargs={'post_id': cls.post.id}
            ): 'posts/post_detail.html',
            reverse('posts:profile', args=[cls.auth]): 'posts/profile.html',
            reverse('posts:post_create'): 'posts/create_post.html',
            reverse(
                'posts:post_edit',
                kwargs={'post_id': cls.post.id}
            ): 'posts/create_post.html'
        }
        cls.reverse_names = (
            reverse('posts:index'),
            reverse(
                'posts:group_list',
                kwargs={'slug': cls.group.slug}
            ),
            reverse('posts:profile', args=[cls.auth])
        )

        cls.form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField
        }

    def setUp(self):
        self.authorized_author = Client()
        self.authorized_author.force_login(PostPagesTests.auth)
        self.user = User.objects.create_user(username='NoName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        for (
            reverse_name,
            template
        ) in PostPagesTests.templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_author.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_create_post_show_correct_context(self):
        """Шаблон create_post сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:post_create'))
        for value, expected in PostPagesTests.form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_edit_show_correct_context(self):
        """Шаблон post_edit сформирован с правильным контекстом."""
        response = self.authorized_author.get(
            reverse(
                'posts:post_edit',
                kwargs={'post_id': PostPagesTests.post.id}
            )
        )
        for value, expected in PostPagesTests.form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_pages_show_correct_context(self):
        """Шаблон index, group_list, profile
        сформированы с правильным контекстом."""
        for reverse_name in PostPagesTests.reverse_names:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                first_object = response.context['page_obj'][0]
                self.assertEqual(
                    first_object.author,
                    PostPagesTests.post.author
                )
                self.assertEqual(first_object.text, PostPagesTests.post.text)
                self.assertEqual(first_object.group, PostPagesTests.post.group)

    def test_post_detail_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse(
                'posts:post_detail',
                kwargs={'post_id': PostPagesTests.post.id}
            )
        )
        self.assertEqual(
            response.context.get('post').text,
            PostPagesTests.post.text
        )
        self.assertEqual(
            response.context.get('post').author,
            PostPagesTests.auth
        )

    def test_post_added_to_page(self):
        """Пост при создании появляется
        на страницах index, group_list, profile"""
        for reverse_name in PostPagesTests.reverse_names:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertIn(
                    PostPagesTests.post,
                    response.context['page_obj'],
                    f'Поста почему-то нет на странице {reverse_name}'
                )

    def test_post_added_correctly_user2(self):
        """Созданный пост не попал в группу, для которой не был предназначен"""
        response = self.authorized_client.get(reverse(
            'posts:group_list',
            kwargs={'slug': PostPagesTests.group_2.slug}
        ))
        self.assertNotIn(
            PostPagesTests.post,
            response.context['page_obj'],
            'Пост есть в этой группе, а не должно быть!'
        )
