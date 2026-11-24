from django.db import models
from core.models import BaseModel
from customers.models import Customer
from products.models import Product


class WishList(BaseModel):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="wishlist_items",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="wishlisted_by",
    )

    class Meta:
        unique_together = ("product", "customer")


class Comment(BaseModel):
    customer = models.ForeignKey(
        "customers.Customer",
        on_delete=models.CASCADE,
        related_name="comments",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    body = models.TextField()

    def __str__(self):
        return f"Comment on {self.product}"