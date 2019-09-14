from django.shortcuts import render
from django.http.response import JsonResponse
from requests import get
from .models import VipUser
import office.dateBaseQuery as query
# Create your views here.
def login(request):
    if request.method == 'POST':
        #获取unionCode
        api = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {
            'appid':'wxd998f218b30a447f',
            'secret':'67f84ebbc2f5c45be7c874fa7ee15acb',
            'js_code':request.POST.get('code'),
            'grant_type':'authorization_code'
            }
        res = get(api,params=payload,verify=False,timeout=3).json()
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
