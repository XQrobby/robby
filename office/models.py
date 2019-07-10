from django.db import models

# Create your models here.
from snack.models import User
from django.utils.timezone import now
#vip用户信息
class VipUserInfo(models.Model):
    agent = models.CharField(verbose_name='服务商',max_length=10,default='NaN')
    vipUserType = models.CharField(verbose_name='用户种类',max_length=10,default='NaN')
    level = models.CharField(verbose_name='技术等级',max_length=4,default='NaN')
    rate = models.FloatField(verbose_name='提成率',default=0)    

class VipUser(User):
    HIRE_STATUS_CHOICES = (
        ('审核中','审核中'),
        ('已就职','已就职'),
        ('已离职','已离职'),
    )
    jobNumber = models.CharField(verbose_name='工号',max_length=10,default='NaN')
    address = models.CharField(verbose_name='地址',max_length=50,default='NaN')
#用户类别系统 重点！！！
    vipUserInfo = models.ForeignKey(VipUserInfo,verbose_name='用户信息',on_delete=models.DO_NOTHING,null=True)
    hiredate = models.DateTimeField(verbose_name='入职时间',blank=True)
    hire = models.CharField(max_length=3,verbose_name='就职状态',default='审核中',choices=HIRE_STATUS_CHOICES)
    dimissionTime = models.DateTimeField(verbose_name='离职时间',blank=True)

    def __str__(self):
        return "-".join(self.jobNumber,self.user.name)