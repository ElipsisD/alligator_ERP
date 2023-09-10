from datetime import datetime

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from rangefilter.filters import DateRangeQuickSelectListFilterBuilder

from erp.models import Transfer, User, Production

admin.site.unregister(Group)
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
        'telegram_username',
        'area',
    )

    fieldsets = (
        (
            'Персональная информация',
            {
                'fields': (
                    'first_name',
                    'last_name',
                    'area',
                )
            },
        ),
        (
            'Telegram',
            {
                'fields': (
                    'chat_id',
                    'telegram_username',
                )
            }
        )
    )

    readonly_fields = (
        'chat_id',
        'telegram_username',
    )

    class Meta:
        model = User


class AbstractAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'author',
        'date',
        'item_number',
        'amount',
        'sender',
        'receiver',
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
        'sender',
        'receiver',
    )
    search_fields = ('item_number',)

    class Meta:
        abstract = True


@admin.register(Transfer)
class TransferAdmin(AbstractAdmin):
    class Meta:
        model = Transfer


@admin.register(Production)
class ProductionAdmin(AbstractAdmin):
    class Meta:
        model = Production
