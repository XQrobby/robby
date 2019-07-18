from django.db import models

# Create your models here.
from snack.models import User
from django.utils.timezone import now
#vip用户信息

class VipUserType(models.Model):
    agent = models.CharField(verbose_name='服务商',max_length=10,default='NaN')
    typ = models.CharField(verbose_name='用户种类',max_length=10,default='NaN')

    def __str__(self):
        return "-".join((self.agent,self.typ))


class Level(models.Model):
    LEVEL_CHOICES = (
        ('大师','大师'),
        ('专家','专家'),
        ('高级','高级'),
        ('中级','中级'),
        ('初级','初级')
    )
    vipUserType = models.ForeignKey(VipUserType,related_name='level',verbose_name='服务商-用户类型',on_delete=models.CASCADE,null=True)
    level = models.CharField(verbose_name='技术等级',max_length=4,default='初级',choices=LEVEL_CHOICES)
    rate = models.FloatField(verbose_name='提成率',default=0)

    def __str__(self):
        return "-".join((self.vipUserType.agent,self.vipUserType.typ,self.level,str(self.rate)))


class VipUser(User):
    HIRE_STATUS_CHOICES = (
        ('审核中','审核中'),
        ('已就职','已就职'),
        ('已离职','已离职'),
    )
    jobNumber = models.CharField(verbose_name='工号',max_length=10,default='NaN')
    address = models.CharField(verbose_name='地址',max_length=50,default='NaN')
#用户类别系统 重点！！！
    level = models.ForeignKey(Level,related_name='vipUser',verbose_name='用户等级',on_delete=models.DO_NOTHING,null=True)
    hiredate = models.DateTimeField(verbose_name='入职时间',null=True)
    hire = models.CharField(max_length=3,verbose_name='就职状态',default='审核中',choices=HIRE_STATUS_CHOICES)
    dimissionTime = models.DateTimeField(verbose_name='离职时间',null=True)

    def __str__(self):
        return "-".join((self.jobNumber,self.name))