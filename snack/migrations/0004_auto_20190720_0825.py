# Generated by Django 2.2.3 on 2019-07-20 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snack', '0003_auto_20190720_0824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='orderLog',
            field=models.TextField(blank=True, verbose_name='订单日志'),
        ),
        migrations.AlterField(
            model_name='order',
            name='serviceLog',
            field=models.TextField(blank=True, verbose_name='服务日志'),
        ),
    ]