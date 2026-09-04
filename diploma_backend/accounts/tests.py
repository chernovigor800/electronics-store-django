from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from accounts.models import ProfileUser

User = get_user_model()


class SignUpAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('sign_up')

    def test_registration_page_exists(self):
        """Тест: страница регистрации доступна"""
        response = self.client.get(self.url)
        # Просто проверяем, что URL существует
        self.assertIn(response.status_code, [200, 405, 400])


class SignInAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('sign_in')
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_successful_login(self):
        """Тест успешного входа"""
        data = {'username': 'testuser', 'password': 'testpass123'}
        response = self.client.post(
            self.url,
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProfileUserAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('profile')
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_get_profile_creates_profile_if_not_exists(self):
        """Тест: при GET запросе создается профиль"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(ProfileUser.objects.filter(user=self.user).exists())