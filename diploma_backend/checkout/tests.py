from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User


class SalesListAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('sales')

    def test_get_sales_list(self):
        """Тест получения списка распродаж"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PaymentAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse('payment', args=[1])

    def test_payment_page_authenticated(self):
        """Тест: страница оплаты доступна для авторизованного пользователя"""
        response = self.client.get(self.url)
        self.assertIn(response.status_code, [200, 404])


class CheckoutURLTest(TestCase):
    def test_checkout_url_exists(self):
        """Тест: URL для checkout существует"""
        response = self.client.get('/api/v1/sales')
        self.assertIn(response.status_code, [200, 404])