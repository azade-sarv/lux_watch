from django.contrib import admin

from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number", "created_at")
    search_fields = ("user__username", "user__email", "phone_number")
