from django import forms
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post

User = get_user_model()


class UsersFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.templates_pages_names = {
            reverse('users:signup'): 'users/signup.html',

        }

    def test_signup_(self):
        """При заполнении формы signup создается новый пользователь"""
        user_count = User.objects.count()
        response = self.client.post(
            reverse('users:signup'),
            data={
                'username': 'NewUser',
                'first_name': 'Имя',
                'last_name': 'Фамилия',
                'email': 'email',
                'password1': 'qwerty12345',
                'password2': 'qwerty12345'
            },
            follow=True
        )
        #self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), user_count + 1)