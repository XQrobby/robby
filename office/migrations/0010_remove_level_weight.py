# Generated by Django 2.2.3 on 2019-07-17 08:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0009_auto_20190717_0853'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='level',
            name='weight',
        ),
    ]