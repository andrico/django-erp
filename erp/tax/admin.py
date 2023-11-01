from django.contrib import admin

from erp.tax.models import Tax
from erp.base_admin import BaseAdmin


admin.site.register(Tax, BaseAdmin)
