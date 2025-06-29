"""
django admin costume user
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core import models 
from django.utils.translation import gettext_lazy as _


class UserAdmin(BaseUserAdmin):
    """
    define the admin page for users
    """
    ordering = ["id"]
    list_display = ["email", "name"]
    fieldsets = (
        (None, {"fields":("email", "password")}),
        (_("permissions"), {"fields": ("is_active", "is_staff", "is_superuser",)}),
        (_("important dates"), {"fields": ("last_login",)}),
            )
    readonly_fields = ["last_login"]
    add_fieldsets = (
        (None, {"classes": ("wide",), 
            "fields": ("email", "password", "password2", "name", "is_staff", "is_superuser",)}),
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Recipe)

