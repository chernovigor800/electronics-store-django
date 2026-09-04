from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.models import ProfileUser
from basket.models import Basket
from orders.models import Order


class CreateOrderAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('orders')
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.profile = ProfileUser.objects.create(
            user=self.user,
            name='John',
            surname='Doe'
        )
        self.client.force_authenticate(user=self.user)

    def test_order_page_authenticated(self):
        """Тест: страница заказов доступна для авторизованного пользователя"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class OrderDetailAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.profile = ProfileUser.objects.create(
            user=self.user,
            name='John',
            surname='Doe'
        )
        self.client.force_authenticate(user=self.user)

        self.basket = Basket.objects.create(user=self.user)
        self.order = Order.objects.create(
            full_name=self.profile,
            city='Moscow',
            delivery_address='Test Street',
            delivery_type='delivery',
            payment_type='online',
            totalCost=2400.00,
            basket=self.basket
        )
        self.url = reverse('order_detail', args=[self.order.id])

    def test_get_order_details(self):
        """Тест получения деталей заказа"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)