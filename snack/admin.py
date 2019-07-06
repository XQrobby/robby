from django.contrib import admin
from .models import ServiceType,Order,Division
# Register your models here.

admin.site.register(ServiceType)
admin.site.register(Order)
admin.site.register(Division)
