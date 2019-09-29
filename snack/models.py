from django.db import models
from office.models import VipUser
# Create your models here.
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


#普通用户属性
class Client(User):
    addrs = models.TextField(verbose_name='报修地址')
    clientID = models.CharField(verbose_name='用户编码',max_length=10,default='NaN')
    section = models.CharField(verbose_name='单位',max_length=20,default='NaN')
    clas = models.CharField(verbose_name='院系/部门',max_length=20,default='NaN')

    def __str__(self):
        return '-'.join((self.name,self.tel[-4:]))

#学校机构
class Division(models.Model):
    section = models.CharField(verbose_name='单位名称',max_length=10,default='NaN')
    clas = models.CharField(verbose_name='部门',max_length=10,default='NaN')

    def __str__(self):
        return '-'.join((self.section,self.clas))
'''
#scholarUser用户属性
class ScholarUser(User):
    division = models.ForeignKey(Division,verbose_name='单位/院系/部门',on_delete=models.DO_NOTHING,blank=True)
    def __str__(self):
        return " ".join((self.user.id,self.user.name,self.clas))
'''

#服务类型
class ServiceType(models.Model):
    typ = models.CharField(verbose_name='服务类型',max_length=10,default='NaN')

    def __str__(self):
        return self.typ

#订单属性
class Order(models.Model):
    ORDER_LEVEL_CHOICES = (
        ('五星','五星'),
        ('四星','四星'),
        ('三星','三星'),
        ('二星','二星'),
        ('一星','一星'),
        ('无','无')
    )
    #订单状态/服务状态 未完成
    ORDER_STATUS_CHOICES = (
        ('审核中','审核中'),
        ('待维修','等待维修'),
        ('已完修','已完修'),
        ('已验收','已验收'),
        ('已撤销','已撤销'),
    )
    SERVICE_STATUS_CHOICES = (
        ('下派中','下派中'),
        ('待维修','待维修'),
        ('维修中','维修中'),
        ('维修完成','维修完成')
    )
    ORDER_TYPE_CHOICES = (
        ('个人订单','个人订单'),
        ('学校订单','学校订单')
    )
    orderID = models.CharField(verbose_name='报修单号',max_length=11,default='NaN')
    client = models.ForeignKey(
        Client,
        verbose_name='客户',
        on_delete=models.DO_NOTHING,
        related_name='order'
    )
    is_assess = models.BooleanField(verbose_name='调度员分配',default=False)
    createTime = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    orderType = models.CharField(verbose_name='订单类型',max_length=4,default='个人订单',choices=ORDER_TYPE_CHOICES)
    technician = models.ForeignKey(VipUser,verbose_name='维修员',on_delete=models.DO_NOTHING,related_name='order',null=True,blank=True)
    serviceType = models.ForeignKey(ServiceType,verbose_name='服务类型',on_delete=models.DO_NOTHING)
    addr = models.CharField(verbose_name='报修地址',max_length=50)
    model = models.CharField(verbose_name='物品型号',max_length=20)
    faultDescription = models.TextField(verbose_name='故障描述',default='NaN')
    faultContent = models.TextField(verbose_name='故障内容',default='NaN')
    costList = models.TextField(verbose_name='维修明细',blank=True)
    add_up = models.CharField(verbose_name='合计',max_length=10,default='0')
    #定义选项
    evaluation = models.CharField(verbose_name='订单评价',blank=True,max_length=200)
    level = models.CharField(verbose_name='星级',max_length=2,choices=ORDER_LEVEL_CHOICES,default='无')
    orderStatus = models.CharField(verbose_name='订单状态',max_length=4,default='审核中',choices=ORDER_STATUS_CHOICES,blank=True)
    orderLog = models.TextField(verbose_name='订单日志',blank=True)
    serviceStatus = models.CharField(verbose_name='服务状态',max_length=4,default='下派中',choices=SERVICE_STATUS_CHOICES)
    serviceLog = models.TextField(verbose_name='服务日志',blank=True)
    cancel = models.BooleanField(verbose_name='撤销',default=False)
    #学校订单属性
    division = models.ForeignKey(Division,verbose_name='单位/院系/部门',on_delete=models.DO_NOTHING,null=True,blank=True)
    audit = models.BooleanField(verbose_name='审核员审核',default=False)
    
    def __str__(self):
        return " ".join((self.orderID,self.serviceType.typ,self.client.name))

def get_photo_path(isinstance,filename):
    productionName = isinstance.orderID
    print(productionName,"",filename)
    return 'images/%s/%s'%(productionName,filename)

class Image(models.Model):
    order = models.ForeignKey(Order,related_name='img',on_delete=models.CASCADE,verbose_name='订单',blank=True,null=True)
    orderID = models.CharField(verbose_name='订单序号',max_length=20)
    image = models.ImageField(upload_to=get_photo_path)
