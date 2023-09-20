from django.contrib import admin
from django.http import HttpRequest


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



