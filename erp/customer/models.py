from django.db import models
from django.conf import settings
from simple_history.models import HistoricalRecords
from django.utils.translation import gettext as _

from erp.base_model import BaseModel


class Customer(BaseModel):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    tax_number = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=_('Tax Number for invoices'),
    )
    phone = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='customers',
        blank=True,
    )

    history = HistoricalRecords()

    def __str__(self):
        return self.name
