"""
Django admin customization.
"""
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser',
            ),
        }),
    )


class PricingOptionInline(admin.TabularInline):
    model = models.PricingOption
    extra = 1


class ToursAdminForm(forms.ModelForm):
    class Meta:
        model = models.Tours
        fields = '__all__'
        widgets = {
            'tags': forms.CheckboxSelectMultiple,
        }


class ToursAdmin(admin.ModelAdmin):
    form = ToursAdminForm
    inlines = [PricingOptionInline]


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Tours, ToursAdmin)
admin.site.register(models.Tag)
