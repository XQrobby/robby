from django.contrib import admin
from .models import ServiceType,Order,Division,Image,Client
from django.utils.html import format_html
from openpyxl import Workbook
from django.http.response import HttpResponse
# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ['orderID','createTime','typ','name','tel','technician','is_assess','orderStatus','serviceStatus','Photo','buttons']
    ordering = ['-createTime']
    '''
    fieldsets = (
        ("订单信息", {'fields': ['orderID', 'client','addr', 'is_assess','orderType','technician',]}),
        ("订单状态", {'fields': ['orderStatus','serviceStatus']}),
        ("订单内容", {'fields':[ ]}),
    )
    '''
    actions = ['export_excel']

    def typ(self,obj):
        return obj.serviceType.typ
    typ.short_description = '订单类别'

    def name(self,obj):
        return obj.client.name
    name.short_description = '用户姓名'

    def tel(self,obj):
        return obj.client.tel
    tel.short_description = '联系电话'

    def buttons(self, obj):
        button_html = ''
        if obj.serviceStatus == '维修完成' and obj.orderStatus == '等待维修':
            button_html = """<a class="changelink" href="/snack/finish_id=%d/">订单完修</a>""" % (
            obj.id)
        elif obj.serviceStatus == '下派中' and obj.orderStatus == '审核中':
            button_html = """<a class="changelink" href="/snack/assess_id=%d/">审核</a>""" % (
                obj.id)
        return format_html(button_html)
    buttons.short_description = "操作"

    def Photo(self,obj):
        button_html = """<a class="changelink" href="/snack/photo=%d/">故障图片</a>""" % (
            obj.id)
        return format_html(button_html)
    Photo.short_description = "图片"

    def export_excel(self,request,queryset):   
        cols = ['序号','服务类别','维修内容','单价','提成率','技术等级']
        meta = self.model._meta
        response = HttpResponse(content_type='application/msexcel')
        wb = Workbook()
        ws = wb.active
        ws.append(cols)
        i = 1
        for obj in queryset:
            serviceType = obj.serviceType.typ
            faultContent = obj.faultContent
            add_up = obj.add_up
            rate = obj.technician.level.rate
            level = obj.technician.level.level
            data = [i,serviceType,faultContent,add_up,rate,level]
            row = ws.append(data)
            i += 1
        wb.save(response)
        return response    
        '''
        content = {
            'serviceType':self.serviceType.typ,
            'faultContent':self.faultContent,
            'add_up':self.add_up,
            'rate':self.technician.level.rate,
            'level':self.technician.level.level,
        }
        '''
        for obj in queryset:
            print(obj.serviceType.typ)

admin.site.register(Client)
admin.site.register(Order,OrderAdmin)
admin.site.register(ServiceType)
admin.site.register(Division)