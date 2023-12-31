from datetime import datetime
from urllib.parse import quote

from admin_interface.models import Theme
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.http import HttpRequest
from django.utils import timezone
from import_export import resources
from import_export.admin import ExportMixin, ImportMixin
from import_export.fields import Field
from rangefilter.filters import DateRangeQuickSelectListFilterBuilder

from erp.enums import WorkArea
from erp.models import Transfer, User, Production, ItemNumber

admin.site.site_title = 'Alligator ERP'
admin.site.index_title = 'Административная панель'
admin.site.site_header = 'ERP'
admin.site.site_url = None
admin.site.unregister(Group)
admin.site.unregister(Theme)


@admin.register(User)
class MyUserAdmin(UserAdmin):
    list_display = (
        'pk',
        'last_name',
        'first_name',
        'patronymic',
        'telegram_username',
        'area',
    )

    def get_fieldsets(self, request: HttpRequest, obj=...):
        if not obj:
            return super().get_fieldsets(request, obj)
        fieldsets = (
            (
                'Персональная информация',
                {
                    'fields': (
                        'first_name',
                        'last_name',
                        'patronymic',
                    )
                },
            ),
        )

        if obj.username:
            return (*fieldsets, (
                'Настройки',
                {
                    'fields': (
                        'is_staff',
                        'username',
                    )
                }
            ))
        return (*fieldsets, (
            'Информация о сотруднике',
            {
                'fields': (
                    'area',
                )
            }
        ),
                (
                    'Telegram',
                    {
                        'fields': (
                            'telegram_username',
                        )
                    }
                ))

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [
                'chat_id',
                'telegram_username',
                'username',
            ]
        else:
            return [
                'chat_id',
                'telegram_username',
            ]

    list_filter = ("is_staff",)

    class Meta:
        model = User


class AbstractAdmin(ExportMixin, admin.ModelAdmin):
    list_display = (
        'id',
        'author',
        'date',
        'item_number',
        'amount',
        'comment',
    )

    list_display_links = (
        'id',
        'author',
        'date',
        'item_number',
    )
    list_filter = (
        (
            'date',
            DateRangeQuickSelectListFilterBuilder(
                title='По дате создания записи',
                default_end=datetime.now(),
            ),
        ),
    )
    search_fields = ('item_number',)
    raw_id_fields = ('item_number',)

    def get_export_filename(self, request, queryset, file_format):
        model_name = quote(self.model._meta.verbose_name_plural.capitalize())
        return f'{model_name} {datetime.now().strftime("%d.%m.%Y %H-%M")}.xlsx'

    def export_action(self, request, *args, **kwargs):
        post = request.POST.copy()
        post['file_format'] = '0'
        request.POST = post
        return super().export_action(request, *args, **kwargs)

    class Meta:
        abstract = True


class AbstractResource(resources.ModelResource):
    item_number = Field(column_name='Номенклатурный номер', attribute='item_number__number')
    amount = Field(column_name='Количество', attribute='amount')
    date = Field(column_name='Дата', attribute='date')

    class Meta:
        abstract = True
        exclude = ('id', 'author', 'comment')

    @staticmethod
    def dehydrate_date(obj: Transfer):
        return timezone.make_naive(obj.date).strftime('%d.%m.%Y %H:%M')


class TransferResource(AbstractResource):
    sender = Field(column_name='Отправитель', attribute='sender')
    receiver = Field(column_name='Получатель', attribute='receiver')

    class Meta:
        model = Transfer
        exclude = ('id', 'author', 'comment')

    @staticmethod
    def dehydrate_sender(obj):
        return WorkArea.get_label_by_name(obj.sender)

    @staticmethod
    def dehydrate_receiver(obj):
        return WorkArea.get_label_by_name(obj.receiver)


class ProductionResource(AbstractResource):
    location = Field(column_name='Цех производства', attribute='location')

    class Meta:
        model = Production
        exclude = ('id', 'author', 'comment')

    @staticmethod
    def dehydrate_location(obj):
        return WorkArea.get_label_by_name(obj.location)


@admin.register(Transfer)
class TransferAdmin(AbstractAdmin):
    resource_class = TransferResource

    list_display = (*AbstractAdmin.list_display, 'sender', 'receiver')
    list_filter = (*AbstractAdmin.list_filter, 'sender', 'receiver')

    class Meta:
        model = Transfer


@admin.register(Production)
class ProductionAdmin(AbstractAdmin):
    resource_class = ProductionResource

    list_display = (*AbstractAdmin.list_display, 'location')
    list_filter = (*AbstractAdmin.list_filter, 'location')

    class Meta:
        model = Production


class ItemNumberResource(resources.ModelResource):
    name = Field(column_name='Наименование', attribute='name')
    number = Field(column_name='Номер', attribute='number')

    class Meta:
        model = ItemNumber
        fields = ('name', 'number')
        import_id_fields = ('number',)
        use_bulk = True
        use_transactions = True
        skip_unchanged = True
        report_skipped = True


@admin.register(ItemNumber)
class ItemNumberAdmin(ImportMixin, admin.ModelAdmin):
    resource_class = ItemNumberResource
    list_display = ('number', 'name')
    list_display_links = ('number',)
    search_fields = ('number', 'name')

    class Meta:
        model = ItemNumber
