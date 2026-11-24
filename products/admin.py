from django.contrib import admin

from .models import (
    Brand,
    Category,
    Product,
    ProductColor,
    ProductImage
)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "created_at")
    search_fields = ("title", "slug")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
        "brand",
        "category",
        "price",
        "is_available",
        "is_special",
        "stash"
    )
    list_filter = (
        "is_available",
        "is_special",
        "is_luxury",
        "brand",
        "category"
    )
    search_fields = (
        "title",
        "slug",
        "brand__name",
        "category__title"
    )
    list_select_related = ("brand", "category")


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("product", "image")
    list_select_related = ("product",)


@admin.register(ProductColor)
class ProductColorAdmin(admin.ModelAdmin):
    list_display = ("product", "color", "hex_code")
    list_select_related = ("product",)