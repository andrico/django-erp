from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

from erp.company.models import Company
from erp.base_admin import BaseAdmin


class CompanyAdmin(BaseAdmin):
    list_display = ('name', 'get_chain', 'phone', 'email', 'address', 'created', 'modified')  # noqa
    search_fields = ('name', 'phone', 'email', 'address')
    list_filter = ('created', 'modified')

    @mark_safe
    def get_chain(self, obj):
        if not obj.chain:
            return '-'
        return self.make_link(
            'admin:company_company_change',
            obj.chain.id,
            obj.chain.name,
        )
    get_chain.short_description = _('Chain')

    fieldsets = (
        (None, {'fields': ('name', 'email', 'phone', 'users', 'chain', 'logo')}),
        (_('Address'), {'fields': ('address', )}),
        (_('Fiscal Data'), {'fields': ('format_invoice_number', 'tax_number', 'taxes')}),  # noqa
        (_('Notes'), {'fields': ('notes', )}),
    )


admin.site.register(Company, CompanyAdmin)
