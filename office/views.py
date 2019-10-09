from django.shortcuts import render
from django.http.response import JsonResponse,HttpResponseRedirect
from requests import get
from .models import VipUser
import office.dateBaseQuery as query
# Create your views here.
def login(request):
    if request.method == 'POST':
        #获取unionCode
        api = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {
            'appid':'wx10a71b42870fba91',
            'secret':'f725c0da9b3b41f8a8b6c98c57e32e7b',
            'js_code':request.POST.get('code'),
            'grant_type':'authorization_code'
            }
        res = get(api,params=payload,verify=False,timeout=3).json()
        print(res)
        #检查User是否存在
        unionCode = res['openid']
        vipUser = query.queryVipUser(unionCode)
        if vipUser:
            vipUser.loginCode = request.POST.get('code')
            vipUser.save()
            userInfoP = {
                'name':vipUser.name,
                'jobNumber':vipUser.jobNumber,
                'address':vipUser.address,
                'agent':vipUser.level.vipUserType.agent,
                'typ':vipUser.level.vipUserType.typ,
                'level':vipUser.level.level,
                'tel':vipUser.tel
            }
            return JsonResponse({
                'status':True,
                'userInfoP':userInfoP,
                'unionCode':unionCode,
            })
        else:
            #用户初始化
            return JsonResponse({'status':'none','vipUserTypes':query.types(),'unionCode':unionCode})
    return JsonResponse({'status':False})

def enroll(requests):
    if requests.method == 'POST':
        content = requests.POST.dict()
        print(content)
        action = query.enroll(content)
        return JsonResponse({'status':True,'action':action})
    else:
        return JsonResponse({'status':False,'action':action})

def taskList(requests):
    if requests.method == 'POST':
        content = requests.POST.dict()
        if query.checkLogin(content['unionCode'],content['code']):
            return JsonResponse({
                'status':True,
                'orders':query.ordersInfo(content['unionCode'],content['showCount'])
                })
    return JsonResponse({'status':False})

def order(request):
    if request.method == 'POST':
        content = request.POST.dict()
        print(content)
        if query.checkLogin(content['unionCode'],content['code']):
            return JsonResponse({'status':True,'order':query.order(content['orderID'])})
    return JsonResponse({'status':False})

def repair(request):
    if request.method == 'POST':
        content = request.POST.dict()
        if query.checkLogin(content['unionCode'],content['code']):
            serviceStatus = query.repair(content['unionCode'],content['orderID'])
            return JsonResponse({'status':True,'serviceStatus':serviceStatus})
    return JsonResponse({'status':False})

def finshRepair(request):
    if request.method == 'POST':
        content = request.POST.dict()
        print(content)
        costList = content['costList'].split(',')
        prices = content['prices'].split(',')
        if query.checkLogin(content['unionCode'],content['code']):
            res = query.finsh_repair(content['unionCode'],content['orderID'],costList,prices,content['faultContent'])
            return JsonResponse({'status':True,'service_status':res})
    return JsonResponse({'status':False})

def complete(request):
    if request.method == 'POST':
        content = request.POST.dict()
        if query.checkLogin(content['unionCode'],content['code']):
            return JsonResponse({'status':True,'costList':query.get_cost_list(content['orderID']),'faultContent':query.get_faultContent(content['orderID'])})
    return JsonResponse({'status':False})

def activate(request,unionCode):
    vipUser = VipUser.objects.get(unionCode=unionCode)
    if vipUser.hire == '审核中' or vipUser.hire == '已离职':
        content = {
            'unionCode':unionCode,
            'name':vipUser.name,
            'tel':vipUser.tel,
            'address':vipUser.address
        }
        return render(request,'activate.html',content)
    return HttpResponseRedirect(redirect_to='/admin/office/vipuser/')

def activate_opt(request):
    if request.method == 'POST':
        content = request.POST.dict()
        res = query.vipUserActivate(content['unionCode'])
        return HttpResponseRedirect(redirect_to='/admin/office/vipuser/')
    return JsonResponse({"status":'can not receive'})


def deactivate(request,unionCode):
    vipUser = VipUser.objects.get(unionCode=unionCode)
    if vipUser.hire == '已就职':
        content = {
            'unionCode':unionCode,
            'name':vipUser.name,
            'tel':vipUser.tel,
            'address':vipUser.address
        }
        return render(request,'deactivate.html',content)
    return HttpResponseRedirect(redirect_to='/admin/office/vipuser/')

def deactivate_opt(request):
    if request.method == 'POST':
        content = request.POST.dict()
        res = query.vipUserDeActivate(content['unionCode'])
        print(res)
        return HttpResponseRedirect(redirect_to='/admin/office/vipuser/')
    return JsonResponse({"status":'can not receive'})
