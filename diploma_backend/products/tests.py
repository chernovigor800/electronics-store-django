from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from products.models import Category, Product


class CategoryListViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('categories')
        Category.objects.create(title='Electronics')

    def test_get_categories_list(self):
        """Тест получения списка категорий"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)


class ProductDetailsAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(title='Electronics')
        self.product = Product.objects.create(
            id=1,
            category=self.category,
            title='Laptop Pro',
            price=1200.00,
            count=10
        )
        self.url = reverse('product_detail', args=[1])

    def test_get_product_details(self):
        """Тест получения деталей товара"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Laptop Pro')


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(title='Electronics')
        self.product = Product.objects.create(
            title='Test Product',
            price=100.00,
            count=5,
            category=self.category
        )

    def test_product_creation(self):
        """Тест создания товара"""
        self.assertEqual(self.product.title, 'Test Product')
        self.assertEqual(self.product.price, 100.00)
        self.assertEqual(self.product.count, 5)
        self.assertEqual(self.product.category.title, 'Electronics')