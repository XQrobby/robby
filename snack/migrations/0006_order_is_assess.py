# Generated by Django 2.2.3 on 2019-07-23 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snack', '0005_auto_20190720_0825'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_assess',
            field=models.BooleanField(default=False, verbose_name='调度员分配'),
        ),
    ]