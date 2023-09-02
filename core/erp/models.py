from django.contrib.auth.models import User
from django.core import validators
from django.db import models

from erp.enums import WorkArea


class Transfer(models.Model):
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='transfers', verbose_name='автор')
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
