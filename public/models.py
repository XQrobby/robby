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
    userType = models.CharField(
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

    def __str__(self):
        return "-".join((str(self.id),self.name,self.userType))


#普通用户属性
class Client(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='cUser')
    userID = models.CharField(verbose_name='用户编码',max_length=10,default='NaN')
    section = models.CharField(verbose_name='单位',max_length=20,default='NaN')
    clas = models.CharField(verbose_name='院系/部门',max_length=20,default='NaN')

#用户地址
class Address(models.Model):
    Client = models.OneToOneField(Client,on_delete=models.CASCADE)
    address = models.CharField(verbose_name='地址',max_length=50,default='NaN')

#vip用户信息
class VipUserInfo(models.Model):
    agent = models.CharField(verbose_name='服务商',max_length=10,default='NaN')
    vipUserType = models.CharField(verbose_name='用户种类',max_length=10,default='NaN')
    level = models.CharField(verbose_name='技术等级',max_length=4,default='NaN')
    rate = models.FloatField(verbose_name='提成率',default=0)    

#vipUser属性
class VipUser(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='vUser')
    jobNumber = models.CharField(verbose_name='工号',max_length=10,default='NaN')
    address = models.CharField(verbose_name='地址',max_length=50,default='NaN')
#用户类别系统 重点！！！
    vipUserInfo = models.ForeignKey(VipUserInfo,verbose_name='用户信息',on_delete=models.DO_NOTHING,blank=True)
    hiredate = models.DateTimeField(verbose_name='入职时间',default=now)
    hire = models.BooleanField(verbose_name='就职状态',default=True)
    dimissionTime = models.DateTimeField(verbose_name='离职时间',blank=True)

    def __str__(self):
        return "-".join(self.jobNumber,self.user.name)

#学校机构
class BelongTo(models.Model):
    section = models.CharField(verbose_name='单位名称',max_length=10,default='NaN')
    clas = models.CharField(verbose_name='院系',max_length=10,default='NaN')

    def __str__(self):
        return '-'.join((self.section,self.clas))

#scholarUser用户属性
class ScholarUser(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='sUser')
    belongTo = models.ForeignKey(BelongTo,verbose_name='单位/院系/部门',on_delete=models.DO_NOTHING,blank=True)
    def __str__(self):
        return " ".join((self.user.id,self.user.name,self.clas))

#服务类型
class ServiceType(models.Model):
    typ = models.CharField(verbose_name='服务类型',max_length=10,default='NaN')

    def __str__(self):
        return self.typ

#订单属性
class Order(models.Model):
    ORDER_LEVEL_CHOICES = (
        ('5','五星'),
        ('4','四星'),
        ('3','三星'),
        ('2','二星'),
        ('1','一星')
    )
    #订单状态/服务状态 未完成
    ORDER_STATUS_CHOICES = (
        ('0','审核中'),
        ('1','等待维修'),
        ('2','已完修'),
        ('3','已验收'),
    )
    SERVICE_STATUS_CHOICES = (
        ('0','下派中'),
        ('1','待维修'),
        ('2','维修中'),
        ('3','维修完成')
    )
    orderID = models.CharField(verbose_name='报修单号',max_length=11,default='NaN')
    client = models.ForeignKey(
        User,
        verbose_name='客户',
        on_delete=models.DO_NOTHING,
        related_name='client'
    )
    technician = models.ForeignKey(
        User,
        verbose_name='维修员',
        on_delete=models.DO_NOTHING,
        related_name='technician',
        blank=True
    )
    serviceType = models.ForeignKey(ServiceType,verbose_name='服务类型',on_delete=models.DO_NOTHING)
    address = models.ForeignKey(Address,verbose_name='报修地址',on_delete=models.DO_NOTHING)
    model = models.CharField(verbose_name='机器型号',max_length=20)
    faultDescription = models.TextField(verbose_name='故障描述')
    #定义选项
    evaluation = models.CharField(verbose_name='订单评价',max_length=200)
    level = models.CharField(verbose_name='星级',max_length=2,choices=ORDER_LEVEL_CHOICES)
    orderStatus = models.CharField(verbose_name='订单状态',max_length=2,choices=ORDER_STATUS_CHOICES)
    orderLog = models.TextField(verbose_name='订单日志')
    serviceStatus = models.CharField(verbose_name='服务状态',max_length=2,choices=SERVICE_STATUS_CHOICES)
    serviceLog = models.TextField(verbose_name='服务日志')

    def __str__(self):
        return " ".join((self.orderID,self.serviceType,self.client.name))

class ScholarOrder(models.Model):
    belongTo = models.ForeignKey(BelongTo,verbose_name='单位/院系/部门',on_delete=models.DO_NOTHING,blank=True)
    audit = models.BooleanField(verbose_name='审核员审核',default=False)

    def __str__(self):
        return " ".join((self.id,self.serviceType,self.client.name))
