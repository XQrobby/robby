# Generated by Django 2.2.3 on 2019-10-10 22:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0016_auto_20191010_2206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vipuser',
            name='level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='员工等级', to='office.Level', verbose_name='用户等级'),
        ),
    ]
