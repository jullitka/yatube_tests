from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Post, Group, User


class PostFormTests(TestCase):
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
            description='Тестовое описание новой группы',
        )
        cls.post = Post.objects.create(
            author=cls.auth,
            text='Тестовый пост',
            group=cls.group
        )

    def setUp(self):
        self.authorized_author = Client()
        self.authorized_author.force_login(PostFormTests.auth)
        self.user = User.objects.create_user(username='NoName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        """Валидная форма создает запись в Post."""
        post_count = Post.objects.count()
        form_data = {
            'text': 'Текст из формы',
            'group': PostFormTests.group.id
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response,
            reverse('posts:profile', args=(self.user,))
        )
        self.assertEqual(Post.objects.count(), post_count + 1)
        self.assertTrue(Post.objects.filter(
            text=form_data['text'],
            group=form_data['group']).exists())

    def test_edit_post(self):
        """Валидная форма изменяет пост в базе данных"""
        post_count = Post.objects.count()
        changed_form_data = {
            'text': 'Текст изменен',
            'group': self.group_2.id,
        }
        response = self.authorized_author.post(reverse(
            'posts:post_edit',
            kwargs={'post_id': PostFormTests.post.id}
        ),
            data=changed_form_data,
            follow=True)
        self.assertRedirects(
            response,
            reverse(
                'posts:post_detail',
                kwargs={'post_id': PostFormTests.post.id}
            )
        )
        self.assertEqual(response.context.get('post'), PostFormTests.post)
        self.assertEqual(Post.objects.count(), post_count)
        self.assertTrue(Post.objects.filter(
            text=changed_form_data['text'],
            group=changed_form_data['group']).exists())
