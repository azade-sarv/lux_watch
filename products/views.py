from django.db.models import F, Avg
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product
from .serializers import (
    LuxurySpecialSerializer,
    ProductDetailSerializer,
    ProductSerializer
)

class ProductListView(APIView):

    def get(self, request):

        products = Product.objects.select_related(
            "brand",
            "category",
        )

        serializer = ProductSerializer(
            products,
            many=True,
        )

        return Response(serializer.data)


class ProductDetailView(APIView):
    def get(self, request, slug):
        product = get_object_or_404(
            Product.objects.select_related(
                "brand",
                "category",
            ).prefetch_related(
                "images",
                "colors",
                "comments__customer__user",
            ),
            slug=slug,
        )

        Product.objects.filter(pk=product.pk).update(
            click_count=F("click_count") + 1
        )
        product.refresh_from_db(fields=["click_count"])

        serializer = ProductDetailSerializer(product)
        return Response(serializer.data)


class LuxurySpecialView(APIView):
    def get(self, request):
        queryset = Product.objects.filter(
            is_special=True,
            is_luxury=True,
            is_available=True,
        )

        average_luxury_price = queryset.aggregate(
            average_luxury_price=Avg("price")
        )["average_luxury_price"]

        serializer = LuxurySpecialSerializer(queryset, many=True)

        return Response({
            "average_luxury_price": average_luxury_price,
            "products": serializer.data,
        })