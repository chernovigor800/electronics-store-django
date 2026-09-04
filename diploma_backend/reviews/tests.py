from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.models import ProfileUser
from products.models import Category, Product


class ProductReviewAPIViewTest(TestCase):
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

        self.category = Category.objects.create(title='Electronics')
        self.product = Product.objects.create(
            id=1,
            category=self.category,
            title='Laptop Pro',
            price=1200.00,
            count=10
        )
        self.url = reverse('product_reviews', args=[1])

    def test_reviews_page_exists(self):
        """Тест: страница отзывов доступна"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_review_requires_auth(self):
        """Тест: добавление отзыва требует авторизации"""
        self.client.force_authenticate(user=None)
        data = {'rate': 5, 'text': 'Great!'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)