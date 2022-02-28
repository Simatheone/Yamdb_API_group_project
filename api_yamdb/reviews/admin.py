from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "bio",
        "role",
        "is_staff",
    )
    search_fields = ("username",)
    list_filter = ("role",)
    empty_value_display = "-пусто-"
