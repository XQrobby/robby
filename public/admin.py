from django.contrib import admin
from .models import User,ServiceType,Order,VipUser,BelongTo,VipUserInfo
# Register your models here.
admin.site.register(User)
admin.site.register(VipUserInfo)
admin.site.register(BelongTo)
admin.site.register(ServiceType)
admin.site.register(Order)
admin.site.register(VipUser)