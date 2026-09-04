from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Basket, BasketItem
from products.models import Product
from products.serializers import ProductSerializer

from .serializers import BasketItemSerializer


class BasketAPIView(APIView):

    def get(self, request):
        if request.user.is_authenticated:
            queryset = BasketItem.objects.filter(basket__user=request.user)
            serializer = BasketItemSerializer(queryset, many=True)
            return Response(serializer.data)

        else:
            basket = request.session.get('basket', {})
            if not basket:
                return Response([])

            result = []
            for product_id_str, quantity in basket.items():
                try:
                    product = Product.objects.get(id=int(product_id_str))
                    data = ProductSerializer(product).data
                    data['count'] = quantity
                    result.append(data)
                except Product.DoesNotExist:
                    pass

            return Response(result)

    def post(self, request):
        product_id = request.data.get('id')
        count = int(request.data.get('count', 1))

        if request.user.is_authenticated:
            basket, _ = Basket.objects.get_or_create(user=request.user)
            product = Product.objects.get(id=product_id)
            basket_item, created = BasketItem.objects.get_or_create(
                basket=basket,
                product=product
            )
            if not created:
                basket_item.quantity += count
            else:
                basket_item.quantity = count
            basket_item.save()

            queryset = BasketItem.objects.filter(basket=basket)
            serializer = BasketItemSerializer(queryset, many=True)
            return Response(serializer.data, status=201)

        else:
            basket = request.session.get('basket', {})
            basket[str(product_id)] = basket.get(str(product_id), 0) + count
            request.session['basket'] = basket

            result = []
            for pid, qty in basket.items():
                try:
                    product = Product.objects.get(id=int(pid))
                    data = ProductSerializer(product).data
                    data['count'] = qty
                    result.append(data)
                except Product.DoesNotExist:
                    pass

            return Response(result, status=201)

    def delete(self, request):
        product_id = request.data.get('id')
        count = int(request.data.get('count', 1))

        if request.user.is_authenticated:
            basket = request.user.basket
            product = Product.objects.get(id=product_id)
            basket_item = BasketItem.objects.get(basket=basket, product=product)

            if basket_item.quantity > count:
                basket_item.quantity -= count
                basket_item.save()
            else:
                basket_item.delete()

            queryset = BasketItem.objects.filter(basket=basket)
            serializer = BasketItemSerializer(queryset, many=True)
            return Response(serializer.data)

        else:
            basket = request.session.get('basket', {})
            key = str(product_id)
            if key in basket:
                if basket[key] > count:
                    basket[key] -= count
                else:
                    del basket[key]
                request.session['basket'] = basket

            result = []
            for pid, qty in basket.items():
                try:
                    product = Product.objects.get(id=int(pid))
                    data = ProductSerializer(product).data
                    data['count'] = qty
                    result.append(data)
                except Product.DoesNotExist:
                    pass

            return Response(result)