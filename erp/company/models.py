from django.db import models
from django.conf import settings
from simple_history.models import HistoricalRecords
from django.utils.translation import gettext as _

from erp.base_model import BaseModel


class Company(BaseModel):
    company = None

    name = models.CharField(
        max_length=255,
        verbose_name=_('Name'),
    )
    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name=_('Email'),
    )
    fantasy_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_('Fantasy Name'),
    )
    tax_number = models.CharField(
        max_length=255,
        help_text=_('Tax Number for invoices'),
        verbose_name=_('Tax Number'),
    )
    phone = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_('Phone Number'),
    )
    address = models.TextField(
        verbose_name=_('Address'),
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Notes'),
    )
    logo = models.ImageField(
        upload_to='company_logos',
        blank=True,
        null=True,
        verbose_name=_('Logo'),
    )

    @property
    def get_logo(self):
        logo = self.logo
        if not logo:
            logo = self.chain.logo
        return logo.url if logo else None
    get_logo.fget.short_description = _('Logo')

    @property
    def get_notes(self):
        notes = self.notes
        if notes == '':
            notes = self.chain.notes
        return notes
    get_notes.fget.short_description = _('Notes')

    @property
    def get_address(self):
        address = self.address
        if not address:
            address = self.chain.address
        return address
    get_address.fget.short_description = _('Address')

    @property
    def get_phone(self):
        phone = self.phone
        if not phone:
            phone = self.chain.phone
        return phone
    get_phone.fget.short_description = _('Phone Number')

    @property
    def get_email(self):
        email = self.email
        if not email:
            email = self.chain.email
        return email
    get_email.fget.short_description = _('Email')

    @property
    def get_tax_number(self):
        tax_number = self.tax_number
        if not tax_number:
            tax_number = self.chain.tax_number
        return tax_number
    get_tax_number.fget.short_description = _('Tax Number')

    @property
    def get_name(self):
        name = self.name
        if not name:
            name = self.chain.name
        return name
    get_name.fget.short_description = _('Name')

    @property
    def get_fantasy_name(self):
        fantasy_name = self.fantasy_name
        if not fantasy_name:
            fantasy_name = self.chain.fantasy_name
        return fantasy_name if fantasy_name else self.get_name
    get_fantasy_name.fget.short_description = _('Fantasy Name')

    format_invoice_number = models.CharField(
        max_length=255,
        help_text=_('Format: {year}-{month}-{day}-{invoice_number}'),
        default='{year}-{month}-{day}-{invoice_number}',
        verbose_name=_('Format Invoice Number'),
    )

    taxes = models.ManyToManyField(
        'tax.Tax',
        related_name='companies',
        blank=True,
        verbose_name=_('Taxes'),
    )

    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='companies',
        blank=True,
        verbose_name=_('Users'),
    )

    chain = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='branches',
        blank=True,
        null=True,
        verbose_name=_('Chain'),
    )

    history = HistoricalRecords()

    def __str__(self):
        if self.fantasy_name:
            return self.fantasy_name

        return self.name

    class Meta:
        verbose_name = _('Company')
        verbose_name_plural = _('Companies')
