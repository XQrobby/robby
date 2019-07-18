from django.contrib import admin
from .models import VipUser,Level,VipUserType
# Register your models here.
admin.site.register(VipUser)
admin.site.register(VipUserType)
admin.site.register(Level)