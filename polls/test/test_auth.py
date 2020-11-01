"""TEST authentication in polls app."""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class AuthenticationTest(TestCase):

    def test_login(self):
        User.objects.create_user(username='lilslimethug', password='12345678', email='eelonino@gmail.com')
        response = self.client.post(reverse('login'), {'username': 'lilslimethug', 'password': '12345678'}, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_login_with_wrong_password(self):
        User.objects.create_user(username='lilslimethug', password='12345678', email='eelonino@gmail.com')
        response = self.client.post(reverse('login'), {'username': 'lilslimethug', 'password': '666'}, follow=True)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_try_to_logged_out(self):
        User.objects.create_user(username='lilslimethug', password='12345678', email='eelonino@gmail.com')
        self.client.login(username='lilslimethug', password='12345678')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
