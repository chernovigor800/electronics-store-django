from django.db.models import Q

from django.conf import settings
from django.core.paginator import Paginator

from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

from .models import Category, Product, Tag
from .serializers import (
    DetailsSerializer,
    TagListSerializer,
    ProductSerializer,
    BannerCategorySerializer,
)


class CategoryListView(APIView):

    def get(self, request):
        categories = Category.objects.filter(parent__isnull=True)
        categories_data = []

        for category in categories:
            children = category.children.all()
            children_data = []

            for child in children:
                data_sub = {
                    "id": child.pk,
                    "title": child.title,
                    "image": child.get_image(),
                    "type": "subcategory"
                }
                children_data.append(data_sub)

            data_cat = {
                "id": category.pk,
                "title": category.title,
                "image": category.get_image(),
                "type": "category",
                "subcategories": children_data
            }
            categories_data.append(data_cat)

        return Response(categories_data)


class CatalogListAPIView(APIView):

    def _get_category_products_ids(self, category_id):
        try:
            Category.objects.get(id=category_id)

            has_children = Category.objects.filter(parent_id=category_id).exists()

            if has_children:
                category_ids = []

                def collect_all_children(cat_id):
                    category_ids.append(cat_id)
                    children = Category.objects.filter(parent_id=cat_id).values_list('id', flat=True)
                    for child_id in children:
                        collect_all_children(child_id)

                collect_all_children(category_id)
                return category_ids
            else:
                return [category_id]

        except Category.DoesNotExist:
            return []

    def filter_queryset(self, products):
        category_id = self.request.GET.get('category')
        min_price = float(self.request.GET.get('filter[minPrice]', 0))
        max_price = float(self.request.GET.get('filter[maxPrice]', float('inf')))
        free_delivery = self.request.GET.get('filter[freeDelivery]', '').lower() == 'true'
        available = self.request.GET.get('filter[available]', '').lower() == 'true'
        name = self.request.GET.get('filter[name]', '').strip()
        tags = self.request.GET.getlist('tags[]')
        sort_field = self.request.GET.get('sort', 'id')
        sort_type = self.request.GET.get('sortType', 'inc')

        if category_id:
            category_ids = self._get_category_products_ids(int(category_id))

            if category_ids:
                products = products.filter(
                    Q(category_id__in=category_ids) |
                    Q(subcategory_id__in=category_ids)
                )
            else:
                products = products.none()

        products = products.filter(price__gte=min_price, price__lte=max_price)

        if free_delivery:
            products = products.filter(freeDelivery=True)

        if available:
            products = products.filter(count__gt=0)

        if name:
            products = products.filter(title__icontains=name)

        if tags:
            for tag in tags:
                products = products.filter(tags__name=tag)

        if sort_type == 'inc':
            products = products.order_by(sort_field)
        else:
            products = products.order_by('-' + sort_field)

        return products

    def get(self, request):
        products = Product.objects.all()
        filtered_products = self.filter_queryset(products)

        page_number = int(request.GET.get('currentPage', 1))
        limit = 6

        paginator = Paginator(filtered_products, limit)
        page = paginator.get_page(page_number)

        products_list = []
        for product in page:
            display_category_id = product.subcategory_id or product.category_id
            display_category_title = (product.subcategory.title if product.subcategory else
                                   product.category.title if product.category else "No category")

            images_list = []
            for image in product.images.all():
                if image.image:
                    images_list.append({
                        "src": image.image.url,
                        "alt": product.title
                    })

            if not images_list:
                images_list.append({
                    "src": settings.MEDIA_URL + "default_none.jpg",
                    "alt": f"{product.title} has no photo"
                })

            products_list.append({
                "id": product.pk,
                "category": display_category_id,
                "categoryName": display_category_title,
                "price": float(product.price),
                "count": product.count,
                "date": product.date.strftime("%Y.%m.%d %H:%M") if product.date else None,
                "title": product.title,
                "description": product.description,
                "freeDelivery": product.freeDelivery,
                "images": images_list,
                "tags": list(product.tags.values_list('name', flat=True)),
                "rating": float(product.rating),
            })

        catalog_data = {
            "items": products_list,
            "currentPage": page_number,
            "lastPage": paginator.num_pages,
            "total": filtered_products.count()
        }

        return Response(catalog_data)


class BannerListAPIView(ListAPIView):
    serializer_class = BannerCategorySerializer

    def get_queryset(self):
        return Category.objects.filter(id=1)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PopularListAPIView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(tags__name__in=['popular'])[:5]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class LimitedListAPIView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(tags__name__in=['limited'])[:5]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ProductDetailsAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = DetailsSerializer
    lookup_url_kwarg = "id"


class TagsListAPIView(ListAPIView):
    serializer_class = TagListSerializer

    def get_queryset(self):
        return Tag.objects.all().distinct()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)