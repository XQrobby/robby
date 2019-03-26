from django.db import models
from django.utils.timezone import now

# Create your models here.
class User(models.Model):
    VIPUSER = 'VU'
    SCHOLARUSER = 'SU'
    USER = 'CU'
    UESR_TYPE_CHOICE = (
        (VIPUSER,'vipUser'),
        (SCHOLARUSER,'scholarUser'),
        (USER,'user'),
    )

    registerTime = models.DateTimeField(verbose_name='注册时间',default=now)
    name = models.CharField(verbose_name='姓名',max_length=10,default='NaN')
    uesrType = models.CharField(
        verbose_name='用户类型',
        max_length=2,
        choices=UESR_TYPE_CHOICE,
        default=USER
    )
    tel = models.CharField(verbose_name='联系电话',max_length=11,default='NaN')
    #微信关于服务器的唯一标识
    unionCode = models.CharField(verbose_name='unionCode',max_length=50,default='NaN')
    #loginCode用于验证用户身份，在登录时更新。appCode==loginCode
    loginCode = models.CharField(verbose_name='微信登录凭证',max_length=50,default='NaN')

#普通用户属性
class Client(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    userID = models.CharField(verbose_name='用户编码',max_length=10,default='NaN')
    section = models.CharField(verbose_name='单位',max_length=20,default='NaN')
    clas = models.CharField(verbose_name='院系/部门',max_length=20,default='NaN')

#用户地址
class Address(models.Model):
    Client = models.OneToOneField(Client,on_delete=models.CASCADE)
    address = models.CharField(verbose_name='地址',max_length=50,default='NaN')

#vipUserType中level属性
class Level(models.Model):
    TECH_GRADE_CHOICES = (
        ('TC_PT','技术实习'),
        ('TC_PM','技术初级'),
        ('TC_TM','技术中级'),
        ('TC_AD','技术高级'),
        ('FN_PT','财务实习'),
        ('FN_DF','财务正式'),
        ('AT_PT','调度实习'),
        ('AT_DF','调度正式'),
        ('VD_PT','销售实习'),
        ('VD_DF','销售正式')
    )
    level = models.CharField(
        verbose_name='技术等级',
        max_length=5,
        choices=TECH_GRADE_CHOICES
    )
    rate = models.FloatField(verbose_name='提成率')

#vip用户类型
class VipUserType(models.Model):
    TECHNICAL = 'TC'
    FINANCE = 'FN'
    ATTEMPER = 'AT'
    VENDITION = 'VD'
    VIPUSER_TYPE_CHOICES = (
        (TECHNICAL,'技术'),
        (FINANCE,'财务'),
        (ATTEMPER,'调度'),
        (VENDITION,'销售')
    )
    typ = models.CharField(verbose_name='用户类别',choices=VIPUSER_TYPE_CHOICES,max_length=2)
    level = models.ForeignKey(Level,verbose_name='技术等级',on_delete=models.DO_NOTHING)
    
#vipUser属性
class VipUser(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    jobNumber = models.CharField(verbose_name='工号',max_length=10,default='NaN')
    address = models.CharField(verbose_name='地址',max_length=50,default='NaN')
#用户类别系统 重点！！！
    level = models.ForeignKey(Level,on_delete=models.DO_NOTHING)
    '''
    vipUserType = models.CharField(
        verbose_name='员工类别',
        max_length=2,
        choices=VIPUSER_TYPE_CHOICES,
        default=TECHNICAL
    )
#用户等级 未完成
    technicalGrade = models.CharField(
        verbose_name='技术等级',
        max_length=2,
        choices=TECH_GRADE_CHOICE[self.vipUserType])
    '''
    hiredate = models.DateTimeField(verbose_name='入职时间',default=now)
    hire = models.BooleanField(verbose_name='就职状态',default=True)
    dimissionTime = models.DateTimeField(verbose_name='离职时间',blank=True)

#clas对象
class Clas(models.Model):
    section = models.ForeignKey(verbose_name='单位')
    clas = models.CharField(verbose_name='院系/部门')

#section对象
class Section(models.Model):
    section = models.CharField(verbose_name='单位名称',max_length=20)

#scholarUser用户属性
class ScholarUser(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    clas = models.ForeignKey(Clas,verbose_name='单位/院系/部门')

#服务类型
class ServiceType(models.Model):
    typ = models.CharField(verbose_name='服务类型',max_length=10)

#订单属性
class Order(models.Model):
    COMMON = 'CO'
    SCHOLAR = 'SC'
    '''
    ORDER_TYPE_CHOICES = (
        (COMMON,'普通'),
        (SCHOLAR,'校方')
    )
    '''
    ORDER_LEVEL_CHOICES = (
        ('5','五星'),
        ('4','四星'),
        ('3','三星'),
        ('2','二星'),
        ('1','一星')
    )
    #订单状态/服务状态 未完成
    ORDER_STATUS_CHOICES = (
        ('','')
    )
    SERVICE_STATUS_CHOICES = (
        ('','')
    )
    orderID = models.CharField(verbose_name='报修单号',max_length=11,default='NaN')
    client = models.ForeignKey(
        User,
        verbose_name='客户',
        on_delete=models.DO_NOTHING,
        related_name='client'
    )
    '''
    orderType = models.CharField(
        verbose_name='订单类型',
        max_length=10,
        choices=ORDER_TYPE_CHOICES
    )
    '''
    serviceType = models.ForeignKey(ServiceType,verbose_name='服务类型',on_delete=models.DO_NOTHING)
    address = models.ForeignObject(Address,verbose_name='报修地址')
    model = models.CharField(verbose_name='机器型号',max_length=20)
    faultDescription = models.TextField(verbose_name='故障描述')
    #定义选项
    evaluation = models.CharField(verbose_name='订单评价',max_length=200)
    level = models.CharField(verbose_name='星级',max_length=2,choices=ORDER_LEVEL_CHOICES)
    orderStatus = models.CharField(verbose_name='订单状态',max_length=2,choices=ORDER_STATUS_CHOICES)
    orderLog = models.TextField(verbose_name='订单日志')
    serviceStatus = models.CharField(verbose_name='服务状态',max_length=2,choices=SERVICE_STATUS_CHOICES)
    serviceLog = models.TextField(verbose_name='服务日志')

class scholarOrder(models.Model):
    clas = models.ForeignKey(Clas,on_delete=models.DO_NOTHING)
    orderType = models.BooleanField(verbose_name='审核员审核',default=False)