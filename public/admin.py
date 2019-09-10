from django.contrib import admin
from .models import ScholarUser,App
from django.utils.html import format_html
# Register your models here.

def user_activate(modeladmin,request,queryset):
    queryset.update(activation=True)
user_activate.short_description = '校方审核员账号激活'

class ScholarUserAdmin(admin.ModelAdmin):
    list_display = ['name','tel','division','activation','buttons']

    def buttons(self, obj):
        button_html = ''
        if obj.activation == False:
            button_html = """<a class="changelink" href="/public/activate_unionCode=%s/">激活</a>""" % (
            obj.unionCode)
        return format_html(button_html)
    buttons.short_description = "操作"

admin.site.register(ScholarUser,ScholarUserAdmin)
admin.site.register(App)