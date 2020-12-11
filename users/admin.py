from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('full_name', 'email', 'is_staff', 'is_active',)
    list_filter = ('full_name', 'email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('full_name', 'email', 'password')}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('full_name', 'email', 'password1', 'password2', 'is_superuser', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)
