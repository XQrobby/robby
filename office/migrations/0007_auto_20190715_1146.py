# Generated by Django 2.2.3 on 2019-07-15 11:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0006_auto_20190715_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='level',
            name='vipUserType',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='level', to='office.VipUserType', verbose_name='服务商-用户类型'),
        ),
    ]
