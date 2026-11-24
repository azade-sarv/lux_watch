from rest_framework import serializers
from customers.models import Customer
from products.models import Product
from .models import Comment, WishList


class CommentSerializer(serializers.ModelSerializer):
    customer_username = serializers.CharField(
        source="customer.user.username",
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = [
            "id",
            "product",
            "customer_username",
            "body",
            "created_at"
        ]


class WishlistProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["title", "slug", "price", "stash", "main_image"]


class WishlistCustomerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Customer
        fields = ["username", "email", "phone_number"]


class WishListSerializer(serializers.ModelSerializer):
    product = WishlistProductSerializer(read_only=True)
    customer = WishlistCustomerSerializer(read_only=True)

    class Meta:
        model = WishList
        fields = ["product", "customer"]
