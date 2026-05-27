from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Order
from basket.models import Basket, BasketItem
from checkout.models import DeliveryPrice
from accounts.models import ProfileUser

from .serializers import OrderSerializer


class CreateOrderAPIView(APIView):

    def get(self, request):
        orders = Order.objects.filter(
            full_name__user=request.user
        ).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            basket = request.user.basket
            profile = ProfileUser.objects.get(user=request.user)
            basket_items = BasketItem.objects.filter(basket=basket)

            if not basket_items.exists():
                return Response({"error": "Empty basket"}, status=400)

            total_cost = sum(item.product.price * item.quantity for item in basket_items)

            order = Order.objects.create(
                full_name=profile,
                basket=basket,
                totalCost=total_cost
            )

            return Response({
                "orderId": order.pk,
                "totalCost": float(total_cost)
            }, status=201)

        except Basket.DoesNotExist:
            return Response({"error": "No basket"}, status=404)
        except ProfileUser.DoesNotExist:
            return Response({"error": "No basket"}, status=404)


class OrderDetailAPIView(APIView):
    def get(self, request, order_id):
        order = Order.objects.get(pk=order_id)
        serializer = OrderSerializer(order)
        return JsonResponse(serializer.data)

    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)

        basket_items = order.basket.baskets.all()
        total_cost = sum(item.product.price * item.quantity for item in basket_items)
        delivery_price = DeliveryPrice.objects.get(id=1)
        has_free_delivery_item = any(item.product.freeDelivery for item in basket_items)

        if total_cost > 2000:
            delivery_cost = 0
        else:
            if has_free_delivery_item:
                delivery_cost = 0
            else:
                delivery_cost = delivery_price.delivery_cost
                delivery_type = request.data["deliveryType"]
                if delivery_type == "express":
                    delivery_cost += delivery_price.delivery_express_cost  # +500₽

        order.totalCost = total_cost + delivery_cost

        order.delivery_type = request.data["deliveryType"]
        order.payment_type = request.data["paymentType"]
        order.city = request.data["city"]
        order.delivery_address = request.data["address"]
        order.status = "accepted"

        order.save()

        return Response({
            "orderId": order.id,
            "totalCost": float(order.totalCost)
        }, status=200)