from collections.abc import Iterator
from typing import Any
from django import forms
from django.contrib import admin
from django.http.request import HttpRequest
from django.urls import path
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from jet.admin import CompactInline

from erp.product.models import (
    Product,
    ProductCategory,
    ProductPrice,
    ProductImage,
    ProductOption,
)
from erp.base_admin import BaseAdmin


class ProductPriceInline(CompactInline):
    model = ProductPrice
    extra = 1
    show_change_link = True

    readonly_fields = ('is_removed', )

    class Meta:
        verbose_name = 'List Price'
        verbose_name_plural = 'List Prices'


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    show_change_link = True
    exclude = ('is_removed', )


class ProductOptionInline(admin.TabularInline):
    model = ProductOption
    extra = 1
    show_change_link = True
    exclude = ('is_removed', )


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class ProductAdmin(BaseAdmin):
    inlines = (ProductPriceInline, ProductImageInline, ProductOptionInline)
    list_display = ('id', 'name', 'price', 'variants', 'add_variant')
    list_display_links = ('id', 'name')
    list_filter = ('categories__name', 'price')
    search_fields = ('name', 'category', 'price')
    form = ProductForm
    readonly_fields = ('variant_of', )
    exclude = ('is_removed', )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj and obj.variant_of:
            form.base_fields['name'].label = 'Variant Name'

        return form

    def get_queryset(self, request, *args, **kwargs):
        queryset = super().get_queryset(request, *args, **kwargs)

        if request.resolver_match.func.__name__ == 'change_view':
            return queryset

        queryset = queryset.filter(variant_of=None)
        return queryset

    @mark_safe
    def add_variant(self, obj):
        if obj.variant_of:
            return ''
        return self.make_link(
            'admin:product_product_add',
            label=_('Add Variant'),
            params={
                'variant_of': obj.id,
                'name': obj.name + ' Variant',
                'price': obj.price,
            },
            as_button=True,
        )
    add_variant.short_description = _('Add Variant')

    @mark_safe
    def variants(self, obj):
        return ', '.join([
            self.make_link('admin:product_product_change', v.id, v.name)
            for v in obj.variants.all()
        ])
    variants.short_description = _('Variants')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'add/variants/',
                self.admin_site.admin_view(self.add_variants),
                name='add-variants',
            ),
        ]
        return custom_urls + urls

    def add_variants(self, request) -> Iterator[Any]:
        variant_of = request.GET.get('variant_of')

        product = self.get_object(request, variant_of)

        context = {
            **self.admin_site.each_context(request),
            'opts': self.model._meta,
            'product': product,
            'variant_of': variant_of,
        }

        return self.add_view(
            request, form_url='', extra_context=context
        )

    def save_model(self, request: HttpRequest, obj: Product, form, change):
        variant_of = request.GET.get('variant_of')
        if not change and variant_of:
            variant_of_obj = Product.objects.get(id=variant_of)
            obj.variant_of = variant_of_obj

        super().save_model(request, obj, form, change)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj=obj)
        if obj and obj.variant_of or request.GET.get('variant_of', None):
            fieldsets[0][1]['fields'] = [
                field for field in fieldsets[0][1]['fields']
                if field != 'categories'
            ]

        return fieldsets


admin.site.register(Product, ProductAdmin)


class ProductCategoryAdmin(BaseAdmin):
    list_display = ('id', 'name', 'parent')
    list_filter = ('name', 'parent')
    search_fields = ('name', 'parent')


admin.site.register(ProductCategory, ProductCategoryAdmin)
