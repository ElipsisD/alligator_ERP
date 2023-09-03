from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models

from erp.enums import WorkArea


class User(AbstractUser):
    chat_id = models.PositiveIntegerField(verbose_name='идентификатор чата')
    telegram_username = models.CharField(max_length=150, verbose_name='username', blank=True, null=True)
    area = models.CharField(choices=WorkArea.choices, max_length=11, verbose_name='место работы', blank=True, null=True)

    class Meta:
        verbose_name = 'сотрудник'
        verbose_name_plural = 'сотрудники'

    def __str__(self):
        return self.get_full_name()


class Transfer(models.Model):
    author = models.ForeignKey(
        to='erp.User', on_delete=models.DO_NOTHING, related_name='transfers', verbose_name='автор'
    )
    date = models.DateTimeField(auto_now_add=True, verbose_name='дата и время')
    item_number = models.CharField(
        max_length=11, validators=[validators.MinLengthValidator(limit_value=11)], verbose_name='номенклатурный номер'
    )
    amount = models.PositiveSmallIntegerField(verbose_name='количество')
    comment = models.TextField(verbose_name='комментарий', blank=True, null=True)
    sender = models.CharField(choices=WorkArea.choices, max_length=11, verbose_name='отправитель')
    receiver = models.CharField(choices=WorkArea.choices, max_length=11, verbose_name='получатель')

    class Meta:
        verbose_name = 'перемещение'
        verbose_name_plural = 'перемещения'

    def __str__(self):
        return f'Перемещение №{self.pk}'
