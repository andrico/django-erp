from django.db.models import Q
from django.urls import reverse
from simple_history.admin import SimpleHistoryAdmin
from model_clone import CloneModelAdminMixin

from erp.company.models import Company
from erp.user.models import User


class BaseAdmin(CloneModelAdminMixin, SimpleHistoryAdmin):
    include_duplicate_action = True
    include_duplicate_object_link = True
    list_display = ('__str__', 'created', 'modified')
    readonly_fields = ('created', 'modified', 'is_removed')
    ordering = ('-created',)

    def get_list_display(self, request):
        if request.user.is_superuser:
            return self.list_display + ('is_removed',)
        return self.list_display

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)

        if self.model == Company:
            return super().get_queryset(request).filter(
                Q(users=request.user) |
                Q(chain__users=request.user)
            ).distinct().all()

        if self.model == User:
            return super().get_queryset(request).filter(
                Q(companies__users=request.user) |
                Q(companies__chain__users=request.user)
            ).distinct().all()

        return super().get_queryset(request).filter(
            Q(company__users=request.user) |
            Q(company__chain__users=request.user)
        ).all()

    def make_link(self, to, id=None, label=None, params=None, as_button=False):
        class_name = 'button' if as_button else ''
        if not label:
            label = 'Edit'

        string_params = ''
        if params:
            string_params = '?' + '&'.join([f'{k}={v}' for k, v in params.items()])  # noqa

        if not id:
            return f'<a class="{class_name}" href="{reverse(to)}{string_params}">{label}</a>'  # noqa

        return f'<a class="{class_name}" href="{reverse(to, args=(id,))}{string_params}">{label}</a>'  # noqa
