from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse


class BasketAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('basket')
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_basket_page_authenticated(self):
        """Тест: страница корзины доступна для авторизованного пользователя"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_basket_page_unauthenticated(self):
        """Тест: страница корзины доступна без авторизации (если так реализовано)"""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        # Ваш API позволяет доступ без авторизации
        self.assertEqual(response.status_code, status.HTTP_200_OK)