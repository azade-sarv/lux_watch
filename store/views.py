from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import WishList
from .serializers import WishListSerializer


class WishlistView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wishlist = (
            WishList.objects
            .filter(customer__user=request.user)
            .select_related("customer__user", "product")
            .order_by("-created_at")
        )

        serializer = WishListSerializer(wishlist, many=True)
        return Response(serializer.data)