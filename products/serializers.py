from rest_framework import serializers

from .models import Product, Brand, Category, ProductImage, ProductColor
from store.serializers import CommentSerializer

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "title", "slug"]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image"]


class ProductColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColor
        fields = ["id", "color", "hex_code"]


class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id", "title", "slug", "price",
            "brand", "category", "is_available", "stash",
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    images = ProductImageSerializer(
        many=True,
        read_only=True,
    )

    colors = ProductColorSerializer(
        many=True,
        read_only=True,
    )

    comments = CommentSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "slug",
            "price",
            "brand",
            "category",
            "is_discount",
            "is_available",
            "is_special",
            "gender",
            "origin",
            "strap_material",
            "usage",
            "design",
            "engine",
            "main_image",
            "features",
            "is_luxury",
            "description",
            "meta_title",
            "meta_description",
            "stash",
            "click_count",
            "created_at",
            "updated_at",
            "images",
            "colors",
            "comments",
        ]


class LuxurySpecialSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            "title",
            "price",
            "gender",
            "strap_material",
            "engine",
        ]