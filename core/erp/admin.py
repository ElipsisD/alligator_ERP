from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from erp.models import Transfer, User


@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):

    class Meta:
        model = Transfer


@admin.register(User)
class MyUserAdmin(UserAdmin):

    list_display = (
        'pk',
        'last_name',
        'first_name',
        'telegram_username',
        'chat_id',
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
