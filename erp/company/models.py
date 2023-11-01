from django.db import models
from django.conf import settings
from simple_history.models import HistoricalRecords
from django.utils.translation import gettext as _

from erp.base_model import BaseModel


class Company(BaseModel):
    company = None

    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    tax_number = models.CharField(
        max_length=255,
        help_text=_('Tax Number for invoices'),
    )
    phone = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField()
    notes = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='company_logos', blank=True, null=True)

    @property
    def get_logo(self):
        logo = self.logo
        if not logo:
            logo = self.chain.logo
        return logo.url if logo else None

    @property
    def get_notes(self):
        notes = self.notes
        if notes == '':
            notes = self.chain.notes
        return notes

    @property
    def get_address(self):
        address = self.address
        if not address:
            address = self.chain.address
        return address

    @property
    def get_phone(self):
        phone = self.phone
        if not phone:
            phone = self.chain.phone
        return phone

    @property
    def get_email(self):
        email = self.email
        if not email:
            email = self.chain.email
        return email

    @property
    def get_tax_number(self):
        tax_number = self.tax_number
        if not tax_number:
            tax_number = self.chain.tax_number
        return tax_number

    format_invoice_number = models.CharField(
        max_length=255,
        help_text=_('Format: {year}-{month}-{day}-{invoice_number}'),
        default='{year}-{month}-{day}-{invoice_number}',
    )

    taxes = models.ManyToManyField(
        'tax.Tax',
        related_name='companies',
        blank=True,
    )

    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='companies',
        blank=True,
    )

    chain = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='branches',
        blank=True,
        null=True,
    )

    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Companies'
