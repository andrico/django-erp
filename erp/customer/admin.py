from django.contrib import admin
from django.utils.translation import gettext as _

from erp.customer.models import Customer
from erp.base_admin import BaseAdmin


class CustomerAdmin(BaseAdmin):
    list_display = ('name', 'phone', 'email', 'address', 'created', 'modified')  # noqa
    search_fields = ('name', 'phone', 'email', 'address')
    list_filter = ('company', 'created')

    fieldsets = (
        (None, {'fields': ('name', 'email', 'phone', 'users', 'company')}),
        (_('Address'), {'fields': ('address', )}),
        (_('Fiscal Data'), {'fields': ('tax_number',)}),  # noqa
        (_('Notes'), {'fields': ('notes', )}),
    )


admin.site.register(Customer, CustomerAdmin)
