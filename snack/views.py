from django.shortcuts import render
from django.http.response import JsonResponse,HttpResponseRedirect
from django.http.request import HttpRequest
from requests import get
from .models import Order,Client
from office.models import VipUser
import snack.dateBaseQuery as query
# Create your views here.
def login(request):
    if request.method == 'POST':
        #获取unionCode
        api = 'https://api.weixin.qq.com/sns/jscode2session'
        payload = {
            'appid':'wxb0b3a42da4af0d73',
            'secret':'5383a21d1b21dcb4f6bf1309a2c2b429',
            'js_code':request.POST.get('code'),
            'grant_type':'authorization_code'
            }
        res = get(api,params=payload,verify=False,timeout=3).json()
        print(res)
            #检查User是否存在
        try:
            unionCode = res['openid']
            client = query.queryClient(unionCode)
        except:
            print('errcode:',res['errcode'])
            return JsonResponse({'status':'请检查appid'})
        if client:
            client.loginCode = request.POST.get('code')
            client.save()
            status = True
            return JsonResponse({
                'status':status,
                'unionCode':unionCode,
                'clientInfoP':query.clientDetail(client),
                'sectionsForm':query.divisionForm(),
                'serviceTypesForm':query.serviceTypeForm()
            })
        else:
            #用户初始化
            #client = query.clientInit(unionCode)
            #client.loginCode = request.POST.get('code')
            status = 'none'
            return JsonResponse({
                'status':status,
                'unionCode':unionCode,
                'sectionsForm':query.divisionForm(),
                'serviceTypesForm':query.serviceTypeForm()
            })
    return JsonResponse({'status':False})

def changeClientInfo(request):
    if request.method == 'POST':
        content = request.POST.dict()
        try:
            if query.checkLogin(content['unionCode'],content['code']):
                query.changeClientInfo(content)
                client = Client.objects.get(unionCode=content['unionCode'])
                return JsonResponse({'status':True,'clientInfoP':query.clientDetail(client)})
            return JsonResponse({'status':False,'detail':'no copyright'})
        except:
            client = query.clientInit(content['unionCode'])
            client.loginCode = content['code']
            client.save()
            query.changeClientInfo(content)
            return JsonResponse({'status':True,'clientInfoP':query.clientDetail(client)})
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
        content = request.POST.dict()
        print(content)
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

def assess(request,order_id):
    order = Order.objects.get(id=order_id)
    if order.is_assess:
        return HttpResponseRedirect(redirect_to='/admin/snack/order/')
    else:
        context = {
            'order_id':order_id,
            'techs':VipUser.objects.filter(hire='已就职')
        }
        return render(request,'order_assess.html',context)

def choiceTech(request):
    if request.method == 'POST':
        if 'tech_id' in request.POST:
            content = request.POST.dict()
            order = Order.objects.get(id=content['order_id'])
            if order.technician:
                pass 
            else:
                query.setTech(content)
    return HttpResponseRedirect(redirect_to='/admin/snack/order/')

def finish(request,order_id):
    context = {'order_id':order_id}
    return render(request,'finish.html',context)

def affirm(request):
    if request.method == 'POST':
        content = request.POST.dict()
        query.affirmFinish(content)
        print(content)
    return HttpResponseRedirect(redirect_to='/admin/snack/order/')

def photo(request,order_id):
    order = Order.objects.get(id=order_id)
    urls = ['/media/'+str(img.image) for img in order.img.all()]
    context = {'urls':urls}
    return render(request,'photos.html',context)

def orderCheck(requests):
    if requests.method == "POST":
        content = requests.POST.dict()
        if query.checkLogin(content['unionCode'],content['code']):
            res = query.orderCheck(content)
        print(requests.POST)
        return JsonResponse({"status":res})
    return JsonResponse({"status":False})