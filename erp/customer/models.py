from django.db import models
from django.conf import settings
from simple_history.models import HistoricalRecords
from django.utils.translation import gettext as _

from erp.base_model import BaseModel


class Customer(BaseModel):
    name = models.CharField(
        max_length=255,
        verbose_name=_('Name'),
    )
    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name=_('Email'),
    )
    tax_number = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=_('Tax Number for invoices'),
    )
    phone = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_('Phone Number'),
    )
    address = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Address'),
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Notes'),
    )

    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='customers',
        blank=True,
        verbose_name=_('Users'),
    )

    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')
