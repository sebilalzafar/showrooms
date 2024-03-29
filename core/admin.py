from django.contrib import admin
from .models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext as _
from .models import User
from django.contrib.auth.forms import AdminPasswordChangeForm


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    
    """Define admin model for custom User model with no email field."""
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('id','first_name', 'last_name',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser','sale_man',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('id','email','first_name','last_name','is_superuser','is_active', 'is_staff', 'sale_man','password1', 'password2',),
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
        (_('Showroom info'), {'fields': ('showroom_type','showroom_name', 'office_phone_number','link_360','google_analytics_link',"address",'since','showroom_owner',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser','sale_man',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('id','email','first_name','last_name','showroom_type','showroom_name','office_phone_number','link_360','google_analytics_link','address','since','showroom_owner','is_superuser','is_active', 'is_staff','sale_man', 'password1', 'password2',),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_superuser','showroom_type','showroom_name')
    search_fields = ('email', 'first_name', 'last_name','showroom_type','showroom_name')
    ordering = ('email',)
    
  




    
admin.site.register(Categories)
admin.site.register(Callback)
admin.site.register(Product)
admin.site.register(Company_name)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(showroom_settings)
admin.site.register(Transaction)
admin.site.register(Node_visitors)