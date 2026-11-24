from django.conf import settings
from django.db import models

from core.models import BaseModel


class Customer(BaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="customer",
    )
    phone_number = models.CharField(max_length=20, blank=True, unique=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username