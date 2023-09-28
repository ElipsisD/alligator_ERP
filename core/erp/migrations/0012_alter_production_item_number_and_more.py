# Generated by Django 4.2.4 on 2023-09-28 11:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0011_itemnumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='production',
            name='item_number',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='erp.itemnumber', verbose_name='номенклатурный номер'),
        ),
        migrations.AlterField(
            model_name='transfer',
            name='item_number',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='erp.itemnumber', verbose_name='номенклатурный номер'),
        ),
    ]