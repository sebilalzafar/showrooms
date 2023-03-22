from django.contrib import admin
from .models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext as _
from .models import User

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('id','first_name', 'last_name',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('id','email','first_name','last_name','is_superuser','is_active', 'is_staff', 'password1', 'password2',),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name',)
    ordering = ('email',)
    
    

@admin.register(Showrooms)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('id','first_name', 'last_name',)}),
        (_('Showroom info'), {'fields': ('showroom_type','showroom_name', 'office_phone_number','link_360',"address",'since','showroom_owner',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('id','email','first_name','last_name','showroom_type','showroom_name','office_phone_number','link_360','address','since','showroom_owner','is_superuser','is_active', 'is_staff', 'password1', 'password2',),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_superuser','showroom_type','showroom_name')
    search_fields = ('email', 'first_name', 'last_name','showroom_type','showroom_name')
    ordering = ('email',)
    
    
admin.site.register(Categories)
admin.site.register(Callback)
admin.site.register(Product)
admin.site.register(Lights)
admin.site.register(Company_name)