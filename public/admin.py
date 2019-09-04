from django.contrib import admin
from .models import ScholarUser,App
# Register your models here.

class ScholarUserAdmin(admin.ModelAdmin):
    list_display = ['name','tel','division','activation']

admin.site.register(ScholarUser,ScholarUserAdmin)
admin.site.register(App)