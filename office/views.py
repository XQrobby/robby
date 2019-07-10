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
            return JsonResponse({
                'status':True,
            })
        else:
            #用户初始化
            return JsonResponse({'status':'none'})
    return JsonResponse({'status':False})