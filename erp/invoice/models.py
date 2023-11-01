import datetime

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.forms import ValidationError
from django.utils.translation import gettext as _
from simple_history.models import HistoricalRecords, HistoricForeignKey
from model_clone.signals import pre_clone_save

from erp.base_model import BaseModel
from erp.product.models import get_product_price
from erp.tax.models import apply_taxes


class Invoice(BaseModel):
    _clone_m2o_or_o2m_fields = ['items']
    _clone_excluded_fields = ['invoice_number']

    customer = HistoricForeignKey(
        'customer.Customer',
        on_delete=models.CASCADE,
        related_name='invoices',
        verbose_name=_('Customer'),
    )
    invoice_number = models.IntegerField(
        verbose_name=_('Invoice Number'),
    )
    date = models.DateField(
        verbose_name=_('Date'),
    )
    due_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_('Due Date'),
    )
    paid = models.BooleanField(
        default=False,
        verbose_name=_('Paid'),
    )
    paid_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_('Paid Date'),
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Notes'),
    )

    taxes = models.ManyToManyField(
        'tax.Tax',
        related_name='invoices',
        blank=True,
        verbose_name=_('Taxes'),
    )

    @property
    def formatted_invoice_number(self):
        company = self.company

        try:
            company = self.company.history.as_of(self.created)
        except Exception:
            pass

        return company.format_invoice_number.format(  # noqa
            year=self.date.year,
            month=self.date.month,
            day=self.date.day,
            invoice_number=f'{self.invoice_number : 08d}',
        ).replace(' ', '')
    formatted_invoice_number.fget.short_description = _('Invoice Number')

    history = HistoricalRecords(inherit=True)

    @property
    def total(self):
        total_taxes = 0
        total = 0
        for item in self.items.all():
            total_taxes += apply_taxes([
                tax.history.as_of(self.created) for tax in
                self.taxes.all()
            ], item.subtotal, True)
            total += item.total

        total += total_taxes
        return round(total, 2)
    total.fget.short_description = _('Total')

    @property
    def subtotal(self):
        subtotal = 0
        for item in self.items.all():
            subtotal += item.subtotal
        return round(subtotal, 2)
    subtotal.fget.short_description = _('Subtotal')

    def __str__(self):
        return f'Invoice: {self.formatted_invoice_number}'

    def clean_fields(self, exclude=None):
        latest_invoice = Invoice.objects.filter(
            customer=self.customer,
        ).order_by('-invoice_number').first()  # noqa

        if latest_invoice and self.date < latest_invoice.date:
            raise ValidationError({
                'date': _(f'Date must be after {latest_invoice.date}'),
            })

        # if not self.pk and not latest_invoice:
        #     self.invoice_number = 1

        # elif not self.pk and latest_invoice:
        #     self.invoice_number = latest_invoice.invoice_number + 1

        super(Invoice, self).clean_fields(exclude)

    class Meta:
        ordering = ['-invoice_number']
        verbose_name = _('Invoice')
        verbose_name_plural = _('Invoices')


@receiver(pre_clone_save, sender=Invoice)
@receiver(pre_save, sender=Invoice)
def invoice_clone_pre_save(sender, instance, **kwargs):
    if instance.pk:
        return

    latest_invoice = Invoice.objects.filter(
        customer=instance.customer,
    ).order_by('-invoice_number').first()

    if latest_invoice:
        instance.invoice_number = latest_invoice.invoice_number + 1
    else:
        instance.invoice_number = 1


@receiver(pre_clone_save, sender=Invoice)
def invoice_date_clone_pre_save(sender, instance, **kwargs):
    instance.date = datetime.date.today()


class InvoiceItem(BaseModel):
    company = None

    invoice = HistoricForeignKey(
        'invoice.Invoice',
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('Invoice'),
    )
    product = HistoricForeignKey(
        'product.Product',
        on_delete=models.CASCADE,
        related_name='invoice_items',
        verbose_name=_('Product'),
    )
    discount = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text=_('Discount in percentage'),
        default=0,
        verbose_name=_('Discount'),
    )

    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name=_('Quantity'),
    )

    @property
    def price(self):
        return get_product_price(self.product.history.as_of(self.created))
    price.fget.short_description = _('Price')

    @property
    def subtotal(self):
        return round(self.quantity * self.price * (1 - self.discount / 100), 2)
    subtotal.fget.short_description = _('Subtotal')

    @property
    def total(self):
        product = self.product
        try:
            product = self.product.history.as_of(self.created)
        except Exception:
            pass

        tax = product.tax

        try:
            tax = tax.history.as_of(self.created)
        except Exception:
            pass

        if not tax:
            return round(self.subtotal, 2)

        return round(tax.apply(self.subtotal), 2)
    total.fget.short_description = _('Total')

    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        super(InvoiceItem, self).save(*args, **kwargs)

    def __str__(self):
        return f'Invoice Item: {self.invoice.invoice_number}'

    class Meta:
        ordering = ['-created']
        verbose_name = _('Invoice Item')
        verbose_name_plural = _('Invoice Items')
