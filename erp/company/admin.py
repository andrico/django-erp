from django.contrib import admin
from django.db.models import Q
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

from erp.company.models import Company
from erp.base_admin import BaseAdmin


class CompanyAdmin(BaseAdmin):
    list_display = ('get_fantasy_name', 'get_chain', 'phone', 'email', 'address', 'created', 'modified')  # noqa
    search_fields = ('name', 'phone', 'email', 'address')
    list_filter = ('chain', 'created')

    @mark_safe
    def get_chain(self, obj):
        if not obj.chain:
            return '-'
        return self.make_link(
            'admin:company_company_change',
            obj.chain.id,
            obj.chain.get_fantasy_name,
        )
    get_chain.short_description = _('Chain')

    fieldsets = (
        (None, {'fields': ('name', 'fantasy_name', 'email', 'phone', 'users', 'chain', 'logo')}),  # noqa
        (_('Address'), {'fields': ('address', )}),
        (_('Fiscal Data'), {'fields': ('format_invoice_number', 'tax_number', 'taxes')}),  # noqa
        (_('Notes'), {'fields': ('notes', )}),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'chain':
            if request and not request.user.is_superuser:
                kwargs['queryset'] = Company.objects.filter(
                    Q(users=request.user) |
                    Q(chain__users=request.user)
                ).distinct().all()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Company, CompanyAdmin)
