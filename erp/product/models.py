from django.db import models
from django.db.models import Q
from django.db.models.constraints import UniqueConstraint
from django.utils.translation import gettext as _
from simple_history.models import HistoricalRecords, HistoricForeignKey

from erp.base_model import BaseModel


class Product(BaseModel):
    name = models.CharField(
        max_length=255,
        verbose_name=_('Name'),
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Description'),
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Price'),
    )
    categories = models.ManyToManyField(
        'ProductCategory',
        related_name='products',
        blank=True,
        verbose_name=_('Categories'),
    )
    tax = HistoricForeignKey(
        'tax.Tax',
        on_delete=models.CASCADE,
        related_name='invoice_items',
        default=None,
        null=True,
        verbose_name=_('Tax'),
    )

    variant_of = HistoricForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='variants',
        blank=True,
        null=True,
        verbose_name=_('Variant Of'),
    )

    history = HistoricalRecords()

    def __str__(self):
        if self.variant_of:
            return f'{self.name} ({self.variant_of.name})'

        return self.name

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')


class ProductImage(BaseModel):
    product = HistoricForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name=_('Product'),
    )
    image = models.ImageField(
        upload_to='product_images',
        verbose_name=_('Image'),
    )
    is_primary = models.BooleanField(
        default=False,
        verbose_name=_('Is Primary'),
    )

    company = None

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
        verbose_name = _('Product Image')
        verbose_name_plural = _('Product Images')


class ProductOption(BaseModel):
    product = HistoricForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='options',
        verbose_name=_('Product'),
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_('Name'),
    )
    value = models.CharField(
        max_length=255,
        verbose_name=_('Value'),
    )

    company = None

    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Product Option')
        verbose_name_plural = _('Product Options')


class ProductCategory(BaseModel):
    name = models.CharField(
        max_length=255,
        verbose_name=_('Name'),
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Description'),
    )
    parent = HistoricForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='children',
        blank=True,
        null=True,
        verbose_name=_('Parent'),
    )
    image = models.ImageField(
        upload_to='product_category_images',
        blank=True,
        null=True,
        verbose_name=_('Image'),
    )

    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Product Category')
        verbose_name_plural = _('Product Categories')


class ListPrice(BaseModel):
    name = models.CharField(
        max_length=255,
        verbose_name=_('Name'),
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Description'),
    )

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
        verbose_name=_('Product'),
    )
    list_price = HistoricForeignKey(
        ListPrice,
        on_delete=models.CASCADE,
        related_name='prices',
        verbose_name=_('List Price'),
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Price'),
    )
    valid_from = models.DateTimeField(
        verbose_name=_('Valid From'),
    )
    valid_to = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_('Valid To'),
    )

    company = None

    history = HistoricalRecords()

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = _('Product Price')
        verbose_name_plural = _('Product Prices')


def get_product_price(product: Product):
    return round(product.price, 2)
