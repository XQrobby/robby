from django.contrib import admin
from .models import User,Agent,VipUserType,Level,Section,Clas,ServiceType,Order
# Register your models here.
admin.site.register(User)
admin.site.register(Agent)
admin.site.register(VipUserType)
admin.site.register(Level)
admin.site.register(Section)
admin.site.register(Clas)
admin.site.register(ServiceType)
admin.site.register(Order)