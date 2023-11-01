from django.db import models
from simple_history.models import HistoricalRecords

from erp.base_model import BaseModel
from erp.product.models import Product, get_product_price


class Tax(BaseModel):
    name = models.CharField(max_length=255)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    subtract = models.BooleanField(default=False)

    def apply(self, amount):
        return apply_taxes([self], amount)

    history = HistoricalRecords()

    def __str__(self):
        return self.name


class TaxGroup(BaseModel):
    name = models.CharField(max_length=255)
    taxes = models.ManyToManyField(
        Tax,
        related_name='groups',
    )

    def apply(self, amount):
        return apply_taxes(self.taxes.all(), amount)

    history = HistoricalRecords()

    def __str__(self):
        return self.name


def apply_taxes(taxes: list[Tax], amount, return_difference=False):
    total = 0 if return_difference else amount
    for tax in taxes:
        if tax.subtract:
            total -= round(amount * tax.percentage / 100, 2)
        else:
            total += round(amount * tax.percentage / 100, 2)

    return total


def total_taxes_grouped(products: list[Product]):
    ret = dict()
    for product in products:
        tax = product.tax
        amount = get_product_price(product)

        if tax.name not in ret:
            ret[tax.name] = 0

        if tax.subtract:
            ret[tax.name] -= round(amount * tax.percentage / 100, 2)
        else:
            ret[tax.name] += round(amount * tax.percentage / 100, 2)

    return ret
