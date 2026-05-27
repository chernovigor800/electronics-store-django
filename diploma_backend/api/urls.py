from django.urls import path

from accounts.views import (
    SignOutAPIView,
    SignInAPIView,
    SignUpAPIView,
    ProfileUserAPIView,
    AvatarChangeAPIView,
    ChangePasswordAPIView,
)
from products.views import (
    CategoryListView,
    CatalogListAPIView,
    BannerListAPIView,
    TagsListAPIView,
    PopularListAPIView,
    LimitedListAPIView,
    ProductDetailsAPIView,
)
from basket.views import BasketAPIView
from orders.views import CreateOrderAPIView, OrderDetailAPIView
from checkout.views import PaymentAPIView, SalesListAPIView
from reviews.views import ProductReviewAPIView


urlpatterns = [
    path('sign-out', SignOutAPIView.as_view()),
    path('sign-in', SignInAPIView.as_view()),
    path('sign-up', SignUpAPIView.as_view()),
    path('profile', ProfileUserAPIView.as_view()),
    path('profile/avatar', AvatarChangeAPIView.as_view()),
    path('profile/password', ChangePasswordAPIView.as_view()),

    path('categories', CategoryListView.as_view()),
    path('catalog', CatalogListAPIView.as_view()),
    path('banners', BannerListAPIView.as_view()),
    path('tags', TagsListAPIView.as_view()),
    path('products/popular', PopularListAPIView.as_view()),
    path('products/limited', LimitedListAPIView.as_view()),
    path('product/<int:id>', ProductDetailsAPIView.as_view()),

    path('basket', BasketAPIView.as_view()),

    path('orders', CreateOrderAPIView.as_view()),
    path('order/<int:order_id>', OrderDetailAPIView.as_view()),

    path('payment/<int:order_id>', PaymentAPIView.as_view()),
    path('sales', SalesListAPIView.as_view()),

    path('product/<int:id>/reviews', ProductReviewAPIView.as_view()),
]
