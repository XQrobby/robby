# Generated by Django 2.2.3 on 2019-10-12 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snack', '0010_client_unionid'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='bookingTime',
            field=models.CharField(default=' ', max_length=20, verbose_name='预计上门时间'),
        ),
    ]
