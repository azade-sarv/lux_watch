from django.contrib import admin

from .models import Comment, WishList


@admin.register(WishList)
class WishListAdmin(admin.ModelAdmin):
    list_display = ("customer", "product", "created_at")
    search_fields = (
        "customer__user__username",
        "customer__user__email",
        "product__slug",
    )
    list_select_related = ("customer__user", "product")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("product", "customer", "created_at")
    search_fields = (
        "body",
        "product__title",
        "customer__user__username",
    )
    list_select_related = ("product", "customer__user")