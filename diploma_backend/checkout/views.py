import datetime

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Sale,  DeliveryPrice, Payment
from products.models import Product
from orders.models import Order
from basket.models import Basket, BasketItem


class SalesListAPIView(APIView):

    def get(self, request):
        page_number = int(request.GET.get('currentPage', 1))
        limit = int(request.GET.get('limit', 20))
        obj_list = []
        for obj in Sale.objects.all():
            obj_list.append(obj)
        paginator = Paginator(obj_list, limit)
        page = paginator.get_page(page_number)
        serialized_data = []

        for sale in page:
            serialized_data.append({
                "id": sale.product.id,
                "price": sale.product.price,
                "salePrice": sale.product.price - sale.discount,
                "dateFrom": sale.date_from,
                "dateTo": sale.date_to,
                "title": sale.product.title,
                "images": [
                    {
                        "src": settings.MEDIA_URL + str(image.image),
                        "alt": sale.product.title,
                    }
                    for image in
                    sale.product.images.all()],
            })
        response_data = {
            "items": serialized_data,
            "currentPage": page_number,
            "lastPage": paginator.num_pages
        }
        return Response(response_data)


class PaymentAPIView(APIView):
    def get(self, request, order_id):
        payment = get_object_or_404(Payment, order__id=order_id)
        order = get_object_or_404(Order, id=order_id)
        return JsonResponse({"status": order.status})

    def post(self, request, order_id):
        data = request.data
        card_number = data['number']
        expiration_month = data['month']
        expiration_year = data['year']
        cvv_code = data['code']
        card_holder_name = data['name']
        current_year = datetime.datetime.now().year % 100


        if int(expiration_year) < current_year or (
                int(expiration_year) == current_year and
                int(expiration_month) < datetime.datetime.now().month):
            order = Order.objects.get(id=order_id)
            order.payment_error = "Payment expired"
            order.save()
            print("payment expired")
            return JsonResponse({"error": "Payment expired"}, status=400)

        if not (len(card_number.strip()) == 16 and card_number.isdigit()):
            print("Card invalid")
            return JsonResponse({"error": "Invalid card number"}, status=400)

        res_date = f"{expiration_month}.{expiration_year}"
        order = Order.objects.get(id=order_id)
        payment = Payment.objects.create(order=order, card_number=card_number, validity_period=res_date)
        order.status = 'paid'
        order.save()

        basket = Basket.objects.get(user=request.user)
        basket_items = BasketItem.objects.filter(basket=basket)
        for basket_item in basket_items:
            product = Product.objects.get(pk=basket_item.product.pk)
            if product.count < basket_item.quantity:
                print("Not enough product items")
                return JsonResponse({"error": "Not enough items in stock"}, status=400)
            product.count -= basket_item.quantity
            product.count_of_orders += 1
            product.save()

        payment.success = True
        payment.save()
        basket_items.delete()
        return HttpResponse(status=200)