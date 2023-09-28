from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core import validators
from django.db import models

from erp.enums import WorkArea


class User(AbstractUser):
    chat_id = models.PositiveIntegerField(verbose_name='идентификатор чата', null=True)
    patronymic = models.CharField(verbose_name="отчество", max_length=150, blank=True)
    telegram_username = models.CharField(max_length=150, verbose_name='username', blank=True, null=True)
    area = models.CharField(choices=WorkArea.choices, max_length=11, verbose_name='место работы', blank=True, null=True)
    username = models.CharField(
        verbose_name="username",
        max_length=150,
        unique=True,
        validators=[UnicodeUsernameValidator()],
        error_messages={"unique": "A user with that username already exists."},
        null=True,
    )

    class Meta:
        verbose_name = 'сотрудник'
        verbose_name_plural = 'сотрудники'

    def __str__(self):
        return self.get_full_name()


class AbstractModel(models.Model):
    date = models.DateTimeField(auto_now_add=True, verbose_name='дата и время')
    item_number = models.ForeignKey(
        to="erp.ItemNumber", verbose_name='номенклатурный номер', on_delete=models.PROTECT
    )
    amount = models.PositiveSmallIntegerField(verbose_name='количество')
    comment = models.TextField(verbose_name='комментарий', blank=True, null=True)

    class Meta:
        abstract = True


class Transfer(AbstractModel):
    author = models.ForeignKey(
        to='erp.User', on_delete=models.CASCADE, related_name='transfers', verbose_name='автор'
    )
    sender = models.CharField(choices=WorkArea.choices, max_length=11, verbose_name='отправитель')
    receiver = models.CharField(choices=WorkArea.choices, max_length=11, verbose_name='получатель')

    class Meta:
        verbose_name = 'перемещение'
        verbose_name_plural = 'перемещения'

    def __str__(self):
        return f'Перемещение №{self.pk}'


class Production(AbstractModel):
    author = models.ForeignKey(
        to='erp.User', on_delete=models.CASCADE, related_name='productions', verbose_name='автор'
    )
    location = models.CharField(choices=WorkArea.choices, max_length=11, verbose_name='цех производства')

    class Meta:
        verbose_name = 'факт производства'
        verbose_name_plural = 'факты производства'

    def __str__(self):
        return f'Факт производства №{self.pk}'


class ItemNumber(models.Model):
    name = models.TextField(verbose_name='наименование номенклатуры')
    number = models.CharField(
        primary_key=True,
        max_length=11,
        validators=[validators.MinLengthValidator(limit_value=11)],
        verbose_name='номер'
    )

    class Meta:
        verbose_name = 'номенклатурный номер'
        verbose_name_plural = 'номенклатурные номера'

    def __str__(self):
        return f'{self.name}'
