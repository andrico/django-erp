from typing import Any
from django.contrib import admin
from django.db.models import Q
from django.http import HttpResponseNotFound
from django.http.request import HttpRequest
from django.utils.safestring import mark_safe
from django.urls import path
from django.utils.translation import gettext as _

from erp.invoice.models import Invoice, InvoiceItem
from erp.base_admin import BaseAdmin
from erp.invoice.helpers import render_to_pdf
from erp.product.models import Product
from erp.tax.models import total_taxes_grouped


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1
    exclude = ('is_removed', )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'product':
            if request and not request.user.is_superuser:
                kwargs['queryset'] = Product.objects.filter(
                    Q(company__users=request.user) |
                    Q(company__chain__users=request.user)
                ).distinct().all()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class InvoiceAdmin(BaseAdmin):
    inlines = [InvoiceItemInline]
    list_display = ('formatted_invoice_number', 'customer', 'date', 'subtotal', 'total', 'paid', 'download')  # noqa
    list_filter = ('customer', 'date', 'paid')
    search_fields = ('customer', 'date', 'paid')
    list_display_links = ('formatted_invoice_number', 'customer')

    exclude = ('invoice_number', )

    fieldsets = (
        (None, {'fields': ('company', 'customer', 'date', 'due_date', 'taxes')}),  # noqa
        (_('Payment'), {'fields': ('paid', 'paid_date')}),
        (_('Notes'), {'fields': ('notes', )}),
    )

    @mark_safe
    def download(self, obj):
        return self.make_link(
            'admin:invoice_pdf',
            obj.id,
            _('Download'),
        )
    download.short_description = _('Download')

    def get_urls(self):
        urls = super().get_urls()
        urls = [
            path(
                '<int:pk>/pdf/',
                self.admin_site.admin_view(self.pdf_view),
                name='invoice_pdf',
            ),
        ] + urls
        return urls

    def pdf_view(self, request, pk):
        invoice = self.get_object(request, pk)
        if not invoice:
            return HttpResponseNotFound('Invoice not found')

        items = invoice.items.filter(
            is_removed=False,
        ).select_related(
            'product',
        ).prefetch_related(
            'product__tax',
        ).all()

        return render_to_pdf(
            'invoice/pdf.html',
            {
                'logo': request.build_absolute_uri(invoice.company.get_logo),
                'invoice': invoice,
                'customer': invoice.customer,
                'company': invoice.company,
                'items': items.all(),
                'taxes': total_taxes_grouped([item.product for item in items.all()]),  # noqa
                'subtotal': invoice.subtotal,
                'total': invoice.total,
            },
            filename=f'INVOICE_{invoice.formatted_invoice_number}.pdf',
            download=True,
        )

    def get_fieldsets(self, request: HttpRequest, obj: Any | None = ...) -> list[tuple[str | None, dict[str, Any]]]:  # noqa
        if request.resolver_match.func.__name__ == 'add_view':
            return (
                (None, {'fields': ('company', 'customer', 'date', 'due_date', 'taxes')}),  # noqa
                (_('Payment'), {'fields': ('paid', 'paid_date')}),
                (_('Notes'), {'fields': ('notes', )}),
            )

        return self.fieldsets

    def save_model(self, request, obj, form, change):
        return super().save_model(request, obj, form, change)


admin.site.register(Invoice, InvoiceAdmin)
