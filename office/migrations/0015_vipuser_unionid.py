# Generated by Django 2.2.3 on 2019-10-10 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0014_auto_20190929_1648'),
    ]

    operations = [
        migrations.AddField(
            model_name='vipuser',
            name='unionID',
            field=models.CharField(default='NaN', max_length=50, verbose_name='unionID'),
        ),
    ]
