from django.db import models

# Create your models here.

from django.utils.timezone import now

class User(models.Model):
    registerTime = models.DateTimeField(verbose_name='注册时间',auto_now_add=True)
    name = models.CharField(verbose_name='姓名',max_length=10,default='NaN')
    tel = models.CharField(verbose_name='联系电话',max_length=11,default='NaN')
    #小程序关于服务器的唯一标识
    unionCode = models.CharField(verbose_name='unionCode',max_length=50,default='NaN')
    #loginCode用于验证用户身份，在登录时更新。appCode==loginCode
    loginCode = models.CharField(verbose_name='微信登录凭证',max_length=50,default='NaN')
    
    class Meta:
        abstract = True


#vip用户信息
class VipUserType(models.Model):
    agent = models.CharField(verbose_name='服务商',max_length=10,default='NaN')
    typ = models.CharField(verbose_name='用户种类',max_length=10,default='NaN')

    def __str__(self):
        return "-".join((self.agent,self.typ))

    class Meta:
        verbose_name = '员工分组'
        verbose_name_plural = '员工分组'


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

    class Meta:
        verbose_name = '员工等级'
        verbose_name_plural = '员工等级'
class VipUser(User):
    HIRE_STATUS_CHOICES = (
        ('审核中','审核中'),
        ('已就职','已就职'),
        ('已离职','已离职'),
    )
    jobNumber = models.CharField(verbose_name='工号',max_length=10,unique=True)
    address = models.CharField(verbose_name='地址',max_length=50,default='NaN')
#用户类别系统 重点！！！
    level = models.ForeignKey(Level,related_name='员工等级',verbose_name='用户等级',on_delete=models.DO_NOTHING,null=True)
    hiredate = models.DateTimeField(verbose_name='入职时间',null=True)
    hire = models.CharField(max_length=3,verbose_name='就职状态',default='审核中',choices=HIRE_STATUS_CHOICES)
    dimissionTime = models.DateTimeField(verbose_name='离职时间',null=True)

    def __str__(self):
        return "-".join((self.jobNumber,self.name))

    class Meta:
        verbose_name = '工作人员'
        verbose_name_plural = '工作人员'