from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


class UserAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["name", "email", "is_staff"]
    list_filter = ["is_staff", "is_superuser"]
    fieldsets = [
        (None, {"fields": ["name", "email"]}),
        ("Personal info", {"fields": ["password"]}),
        ("Permissions", {"fields": ["is_staff", "is_superuser"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": [
                    "name",
                    "email",
                    "password1",
                    "password2"
                ],
            },
        ),
    ]
    search_fields = ["name", "email"]
    ordering = ["email"]
    filter_horizontal = []


admin.site.register(User, UserAdmin)


