# Generated by Django 2.2.3 on 2019-09-29 16:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snack', '0008_auto_20190929_1220'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={'verbose_name': '客户', 'verbose_name_plural': '客户'},
        ),
        migrations.AlterModelOptions(
            name='division',
            options={'verbose_name': '学校机构', 'verbose_name_plural': '学校机构'},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': '订单', 'verbose_name_plural': '订单'},
        ),
        migrations.AlterModelOptions(
            name='servicetype',
            options={'verbose_name': '服务类型', 'verbose_name_plural': '服务类型'},
        ),
    ]
