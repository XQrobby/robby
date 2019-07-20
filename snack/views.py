from django.shortcuts import render
from django.http.response import JsonResponse
from django.http.request import HttpRequest
from requests import get
from .models import Order
import snack.dateBaseQuery as query
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
        client = query.queryClient(unionCode)
        if client:
            client.loginCode = request.POST.get('code')
            client.save()
            status = True
        else:
            #用户初始化
            client = query.clientInit(unionCode)
            client.loginCode = request.POST.get('code')
            status = 'none'
        return JsonResponse({
            'status':status,
            'clientInfoP':query.clientDetail(client),
            'sectionsForm':query.divisionForm(),
            'serviceTypesForm':query.serviceTypeForm()
        })
    return JsonResponse({'status':False})

def changeClientInfo(request):
    if request.method == 'POST':
        content = request.POST.dict()
        if query.checkLogin(content['unionCode'],content['code']):
            query.changeClientInfo(content)
            return JsonResponse({'status':True})
        return JsonResponse({'status':False,'detail':'no copyright'})
    return JsonResponse({'status':False})

def newOrder(request):
    if request.method == 'POST':
        content = request.POST.dict()
        if query.checkLogin(content['unionCode'],content['code']):
            return JsonResponse({'status':True,'orderID':query.nOrder(content)})
    return JsonResponse({'status':False})

def orderPic(request):
    if request.method == 'POST':
        content = request.POST.dict()
        if query.checkLogin(content['unionCode'],content['code']):
            query.receiveImage(request.FILES['file'],content['orderID'])
            return JsonResponse({'status':'success'})
    return JsonResponse({'status':False})

def orderList(request):
    if request.method == 'POST':
        unionCode = request.POST.get('unionCode')
        count = request.POST.get('showCount')
        if query.checkLogin(unionCode,request.POST.get('code')):
            return JsonResponse({'status':True,'orders':query.ordersInfo(unionCode,count)})
    return JsonResponse({'status':False})

def order(request):
    if request.method == 'POST':
        content = request.POST.dict()
        if query.checkLogin(content['unionCode'],content['code']):
            
            return JsonResponse({'status':True,'order':query.order(content['orderID'])})
    return JsonResponse({'status':False})

def cancel(request):
    if request.method == 'POST':
        content = request.POST.dict()
        if query.checkLogin(content['unionCode'],content['code']):
            return JsonResponse({'status':query.cancel(content['orderID'],content['unionCode'])})
    return JsonResponse({'status':False})