import json
import os

from django.conf import settings
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import ProfileForm
from .models import ProfileUser
from products.models import Product
from basket.models import Basket, BasketItem
from .serializers import ProfileSerializer, UserCreateSerializer


class SignUpAPIView(APIView):
    def post(self, request):
        print("Request.data:", request.data)

        json_string = None
        if request.data:
            first_value = list(request.data.values())[0]
            if first_value and first_value[0] and first_value[0].strip():
                json_string = first_value[0]
            elif list(request.data.keys())[0].strip():
                json_string = list(request.data.keys())[0]

        print("JSON string:", json_string)

        if not json_string:
            return Response({'error': 'No JSON data'}, status=400)

        try:
            data = json.loads(json_string)
            print("Parsed data:", data)
        except json.JSONDecodeError:
            return Response({'error': 'Wrong JSON'}, status=400)


        serializer = UserCreateSerializer(data=data)

        if serializer.is_valid():
            user = serializer.create(serializer.validated_data)

            return Response({
                'message': 'success',
                'username': user.username
            }, status=201)

        return Response(serializer.errors, status=400)


class SignInAPIView(APIView):
    def post(self, request):
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)

            session_basket = request.session.get('basket', {})
            if session_basket:
                user_basket, _ = Basket.objects.get_or_create(user=user)
                for product_id_str, quantity in session_basket.items():
                    try:
                        product_id = int(product_id_str)
                        product = Product.objects.get(id=product_id)
                        user_item, created = BasketItem.objects.get_or_create(
                            basket=user_basket,
                            product=product,
                            defaults={'quantity': quantity}
                        )
                        if not created:
                            user_item.quantity += quantity
                            user_item.save()
                    except Product.DoesNotExist:
                        pass

                del request.session['basket']

            return Response({'status': 'success'})
        return Response({'error': 'Wrong data'}, status=401)


class SignOutAPIView(APIView):
    def post(self, request):
        logout(request)
        return Response({'status': 'success'})


class ProfileUserAPIView(APIView):

    def get(self, request):
        profile, created = ProfileUser.objects.get_or_create(user=request.user)

        if created:
            profile.save()

        print(profile.avatar)
        serializer = ProfileSerializer(profile)
        print(serializer.data)
        return Response(serializer.data)

    def post(self, request):
        full_name = request.data.get('fullName', '').strip().split()

        if len(full_name) >= 3:
            surname, name, patronymic = full_name[:3]
        elif len(full_name) >= 2:
            surname, name = full_name
            patronymic = ''
        else:
            surname = full_name[0] if full_name else ''
            name = patronymic = ''

        phone = request.data.get('phone', '')
        email = request.data.get('email', '')

        profile, created = ProfileUser.objects.get_or_create(user=request.user)
        profile.surname = surname
        profile.name = name
        profile.patronymic = patronymic
        profile.phone = phone
        profile.email = email
        profile.save()

        if email and email != request.user.email:
            request.user.email = email
            request.user.save()

        serializer = ProfileSerializer(profile)
        return Response(serializer.data)


class AvatarChangeAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        user_profile = ProfileUser.objects.get(user=request.user)
        avatar_file = request.FILES.get('avatar')
        avatar_path = os.path.join(settings.MEDIA_ROOT, str(user_profile.avatar))

        if avatar_file:
            if os.path.isfile(avatar_path) and user_profile.avatar != 'avatar_default.jpg':
                os.remove(avatar_path)

        form = ProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return Response(status=200)
        return Response(status=500)


class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        user = request.user
        current_password = request.data.get('currentPassword')
        new_password = request.data.get('newPassword')

        if user.check_password(current_password):
            user.set_password(new_password)
            user.save()
            return Response(status=200)
        return Response(status=500)
