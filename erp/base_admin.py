from simple_history.admin import SimpleHistoryAdmin
from django.urls import reverse
from model_clone import CloneModelAdminMixin


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
        return super().get_queryset(request).objects_not_deleted.all()

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
