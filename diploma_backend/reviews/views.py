from rest_framework.response import Response

from .models import Review

from accounts.models import ProfileUser

from products.models import Product
from products.views import ProductDetailsAPIView


class ProductReviewAPIView(ProductDetailsAPIView):

    def post(self, request, **kwargs):

        if request.user.is_authenticated:
            profile = ProfileUser.objects.get(user=request.user)
            product = Product.objects.get(pk=kwargs['id'])

            review_author_name = request.data.get('author', '').strip() or profile.name
            review_author_email = request.data.get('email', '').strip()
            text = request.data.get('text', '').strip()
            rate = int(request.data.get('rate', 0))

            Review.objects.create(
                author=profile,
                product=product,
                text=text,
                rate=rate,
                review_author_name=review_author_name,
                review_author_email=review_author_email
            )

            return Response({
                "status": "success",
                "message": "Review created!",
                "new_review": {
                    "author": review_author_name,
                    "email": review_author_email,
                    "text": text,
                    "rate": rate
                }
            }, status=201)

        return Response({"error": "No authorization"}, status=403)





