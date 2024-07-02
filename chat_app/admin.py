from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


class CustomUserAdmin(UserAdmin):
    """Define admin model for custom User model with no username field."""
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name','username','image')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser','is_admin',
                                       'groups','user_permissions',)}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('id','email', 'username', 'last_name',)
    search_fields = ('email', 'first_name', 'last_name','username')
    ordering = ('email',)
    
admin.site.register(get_user_model(), CustomUserAdmin)