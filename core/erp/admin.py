from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from erp.models import Transfer, User


@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):

    class Meta:
        model = Transfer


@admin.register(User)
class MyUserAdmin(UserAdmin):

    class Meta:
        model = User
