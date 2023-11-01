from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.utils.translation import gettext as _

from erp.user.models import User
from erp.base_admin import BaseAdmin


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class UserAdmin(BaseAdmin, UserAdmin):
    list_display = ('email', 'full_name', 'is_staff', 'is_superuser')  # noqa
    list_filter = ('companies', 'is_staff', 'is_superuser')
    search_fields = ('email',)
    form = CustomUserChangeForm
    list_display_links = ('email', 'full_name')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2'),
            },
        ),
    )


admin.site.register(User, UserAdmin)
