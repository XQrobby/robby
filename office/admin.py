from django.contrib import admin
from .models import VipUser,Level,VipUserType
from django.utils.html import format_html
# Register your models here.

class VipUserAdmin(admin.ModelAdmin):
    list_display = ['jobNumber','name','hire','tel','hiredate','level','buttons']

    def buttons(self, obj):
        button_html = ''
        if obj.hire == '审核中' or obj.hire == '已离职':
            button_html = """<a class="changelink" href="/office/activate_unionCode=%s/">激活</a>""" % (
            obj.unionCode)
        elif obj.hire == '已就职':
            button_html = """<a class="changelink" href="/office/deactivate_unionCode=%s/">离职</a>""" % (
                obj.unionCode)
        return format_html(button_html)
    buttons.short_description = "操作"

admin.site.register(VipUser,VipUserAdmin)
admin.site.register(VipUserType)
admin.site.register(Level)