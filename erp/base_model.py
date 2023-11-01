from django.db import models
from django.utils.translation import gettext as _
from model_utils.models import (
    QueryManager,
    SoftDeletableModel,
    TimeStampedModel,
)
from model_clone import CloneMixin
from simple_history.models import HistoricForeignKey


class BaseModel(CloneMixin, TimeStampedModel, SoftDeletableModel):

    objects_not_deleted = QueryManager(is_removed=False)

    company = HistoricForeignKey(
        'company.Company',
        on_delete=models.CASCADE,
        related_name='%(class)ss',
        verbose_name=_('Company'),
    )

    class Meta:
        abstract = True
        ordering = ['-created']
