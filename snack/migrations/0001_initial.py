# Generated by Django 2.2.3 on 2019-07-20 08:20

from django.db import migrations, models
import django.db.models.deletion
import snack.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registerTime', models.DateTimeField(auto_now_add=True, verbose_name='注册时间')),
                ('name', models.CharField(default='NaN', max_length=10, verbose_name='姓名')),
                ('tel', models.CharField(default='NaN', max_length=11, verbose_name='联系电话')),
                ('unionCode', models.CharField(default='NaN', max_length=50, verbose_name='unionCode')),
                ('loginCode', models.CharField(default='NaN', max_length=50, verbose_name='微信登录凭证')),
                ('addrs', models.TextField(verbose_name='报修地址')),
                ('clientID', models.CharField(default='NaN', max_length=10, verbose_name='用户编码')),
                ('section', models.CharField(default='NaN', max_length=20, verbose_name='单位')),
                ('clas', models.CharField(default='NaN', max_length=20, verbose_name='院系/部门')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Division',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', models.CharField(default='NaN', max_length=10, verbose_name='单位名称')),
                ('clas', models.CharField(default='NaN', max_length=10, verbose_name='部门')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderID', models.CharField(max_length=20, verbose_name='订单序号')),
                ('image', models.ImageField(upload_to=snack.models.get_photo_path)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typ', models.CharField(default='NaN', max_length=10, verbose_name='服务类型')),
            ],
        ),
        migrations.CreateModel(
            name='ScholarUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registerTime', models.DateTimeField(auto_now_add=True, verbose_name='注册时间')),
                ('name', models.CharField(default='NaN', max_length=10, verbose_name='姓名')),
                ('tel', models.CharField(default='NaN', max_length=11, verbose_name='联系电话')),
                ('unionCode', models.CharField(default='NaN', max_length=50, verbose_name='unionCode')),
                ('loginCode', models.CharField(default='NaN', max_length=50, verbose_name='微信登录凭证')),
                ('division', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, to='snack.Division', verbose_name='单位/院系/部门')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderID', models.CharField(default='NaN', max_length=11, verbose_name='报修单号')),
                ('createTime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('orderType', models.CharField(choices=[('个人订单', '个人订单'), ('学校订单', '学校订单')], default='个人订单', max_length=4, verbose_name='订单类型')),
                ('addr', models.CharField(max_length=50, verbose_name='报修地址')),
                ('model', models.CharField(max_length=20, verbose_name='物品型号')),
                ('faultDescription', models.TextField(default='NaN', verbose_name='故障描述')),
                ('faultContent', models.TextField(default='NaN', verbose_name='故障内容')),
                ('costList', models.TextField(default='NaN', verbose_name='维修明细')),
                ('evaluation', models.CharField(max_length=200, verbose_name='订单评价')),
                ('level', models.CharField(blank=True, choices=[('五星', '五星'), ('四星', '四星'), ('三星', '三星'), ('二星', '二星'), ('一星', '一星')], max_length=2, verbose_name='星级')),
                ('orderStatus', models.CharField(blank=True, choices=[('审核中', '审核中'), ('等待维修', '等待维修'), ('已完修', '已完修'), ('已验收', '已验收'), ('已撤销', '已撤销')], default='审核中', max_length=4, verbose_name='订单状态')),
                ('orderLog', models.TextField(verbose_name='订单日志')),
                ('serviceStatus', models.CharField(choices=[('下派中', '下派中'), ('待维修', '待维修'), ('维修中', '维修中'), ('维修完成', '维修完成')], default='下派中', max_length=4, verbose_name='服务状态')),
                ('serviceLog', models.TextField(verbose_name='服务日志')),
                ('cancel', models.BooleanField(default=False, verbose_name='撤销')),
                ('audit', models.BooleanField(default=False, verbose_name='审核员审核')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='order', to='snack.Client', verbose_name='客户')),
                ('division', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='snack.Division', verbose_name='单位/院系/部门')),
                ('serviceType', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='snack.ServiceType', verbose_name='服务类型')),
            ],
        ),
    ]