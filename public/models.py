from django.db import models
from django.utils.timezone import now
from snack.models import Division

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

#ScholarUser
class ScholarUser(User):
    division = models.ForeignKey(Division,verbose_name='单位/院系/部门',on_delete=models.DO_NOTHING,blank=True)
    activation = models.BooleanField(verbose_name='用户激活',default=False)

class AssessToken(models.Model):
    access_token = models.TextField(verbose_name='api调用凭证',default="NaN")
    save_time = models.DateTimeField(verbose_name='保存时间',auto_now=True)
    data_line = models.DateTimeField(verbose_name='最后有效时间',blank=True,null=True)


class App(models.Model):
    appid = models.CharField(default='NaN',max_length=100)
    secret = models.CharField(default='NaN',max_length=100)