from datetime import datetime

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.http import HttpRequest
from import_export.fields import Field
from rangefilter.filters import DateRangeQuickSelectListFilterBuilder
from django.contrib.admin import sites
from import_export.admin import ExportMixin
from import_export import resources

from erp.enums import WorkArea
from erp.models import Transfer, User, Production


class MyAdminSite(admin.AdminSite):

    def get_app_list(self, request: HttpRequest, app_label: str | None = ...):
        apps = [
            {
                'name': 'ссылки',
                'models': [
                    {'name': 'Telegram', 'perms': {'View': True}, 'admin_url': 'https://t.me/erp_developing_bot'},
                ]
            }
        ]
        return apps + super().get_app_list(request)


myadmin = MyAdminSite()
admin.site = myadmin
sites.site = myadmin

admin.site.site_title = 'Alligator ERP'
admin.site.index_title = 'Административная панель'
admin.site.site_header = 'Alligator ERP'
admin.site.site_url = None


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

    def get_export_filename(self, request, queryset, file_format):
        return f'{self.model.__name__} {datetime.now().strftime("%d.%m.%Y %H-%M")}.xlsx'

    def export_action(self, request, *args, **kwargs):
        post = request.POST.copy()
        post['file_format'] = '0'
        request.POST = post
        return super().export_action(request, *args, **kwargs)

    class Meta:
        abstract = True


class AbstractResource(resources.ModelResource):
    item_number = Field(column_name='Номенклатурный номер', attribute='item_number')
    amount = Field(column_name='Количество', attribute='amount')
    date = Field(column_name='Дата', attribute='date')

    class Meta:
        abstract = True
        exclude = ('id', 'author', 'comment')

    @staticmethod
    def dehydrate_date(obj: Transfer):
        return obj.date.strftime('%d.%m.%Y %H:%M')


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
