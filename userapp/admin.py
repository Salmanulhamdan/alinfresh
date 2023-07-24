from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from .models import *


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'name', 'phone_number', 'is_staff', )
    list_filter = ('is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'phone_number')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'phone_number', 'password'),
        }),
    )
    search_fields = ('email', 'name', 'phone_number')
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)


admin.site.register(Address)
admin.site.register(Wallet)


