from django.db import models
from django.db.models import Q
from django.db.models.constraints import UniqueConstraint
from django.utils.translation import gettext as _
from simple_history.models import HistoricalRecords, HistoricForeignKey

from erp.base_model import BaseModel


class Product(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    categories = models.ManyToManyField(
        'ProductCategory',
        related_name='products',
        blank=True,
    )
    tax = HistoricForeignKey(
        'tax.Tax',
        on_delete=models.CASCADE,
        related_name='invoice_items',
        default=None,
        null=True,
    )

    variant_of = HistoricForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='variants',
        blank=True,
        null=True,
    )

    history = HistoricalRecords()

    def __str__(self):
        if self.variant_of:
            return f'{self.name} ({self.variant_of.name})'

        return self.name


class ProductImage(BaseModel):
    product = HistoricForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
    )
    image = models.ImageField(upload_to='product_images')
    is_primary = models.BooleanField(default=False)

    history = HistoricalRecords()

    def __str__(self):
        return self.product.name

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=[
                    'is_primary',
                    'product',
                ],
                condition=Q(is_primary=True),
                name='unique_is_primary',
            )
        ]


class ProductOption(BaseModel):
    product = HistoricForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='options',
    )
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Product Option')
        verbose_name_plural = _('Product Options')


class ProductCategory(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    parent = HistoricForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='children',
        blank=True,
        null=True,
    )
    image = models.ImageField(
        upload_to='product_category_images',
        blank=True,
        null=True,
    )

    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Product Category')
        verbose_name_plural = _('Product Categories')


class ListPrice(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('List Price')
        verbose_name_plural = _('List Prices')


class ProductPrice(BaseModel):
    product = HistoricForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='prices',
    )
    list_price = HistoricForeignKey(
        ListPrice,
        on_delete=models.CASCADE,
        related_name='prices',
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField(blank=True, null=True)

    history = HistoricalRecords()

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = _('Product Price')
        verbose_name_plural = _('Product Prices')


def get_product_price(product: Product):
    return round(product.price, 2)
