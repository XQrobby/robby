from django.shortcuts import render
from django.http.response import HttpResponse,JsonResponse,HttpResponseRedirect
from wechatpy import parse_message,create_reply
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.utils import check_signature
import public.dateBaseQuery as query
import hashlib
import public.response as rspon
from requests import post,get
from .models import App,ScholarUser
from snack.dateBaseQuery import divisionForm
import datetime
import logging
# Create your views here.
collect_logger = logging.getLogger('scripts')
'''
WECHAT_TOKEN = 'hello'
def wechat(request):
    if request.method == 'GET':
        signature = reqeust.GET.get('signature','')
        timestamp = request.GET.get('timestamp','')
        nonce = request.GET.get('nonce','')
        echo_str = request.GET.get('echostr','')
        try:
            check_signature(WECHAT_TOKEN,signature,timestamp,nonce)
        except IndentationError:
            echo_str = 'error'
        response = HttpResponse(echo_str,content_type="text/plain")
        return response
    elif request.method == 'POST':
        msg = parse_message(request.body)
        if msg.type == 'text':
            reply = create_reply('这是条文字消息',msg)
        elif msg.type == 'image':
            reply = create_reply('这是条图片消息',msg)
        elif msg.type == 'voice':
            reply = create_reply('这是条语音消息',msg)
        else:
            reply = create_reply('这是条其他类型消息',msg)
        response = HttpResponse(reply.render(),content_type='application/xml')
        return response
    else:
        logger.info('-----------------')    
'''

def develop(request):
    if request.method == "GET":
        token = 'robbyHtml'
        #计算加密
        content = request.GET.dict()
        sha1 = hashlib.sha1()
        arr = [content['timestamp'],content['nonce'],token]
        arr.sort()
        sha1.update(''.join(arr).encode('utf-8'))
        sha1Str = sha1.hexdigest()
        print(sha1Str == content['signature'],content)
        #验证签名
        if sha1Str == content['signature']:
            return HttpResponse(content['echostr'])
        return JsonResponse({"status":False})
    elif request.method == 'POST':
        print('body:',request.body,'\npost:',dir(request),'\nfiles:',request.FILES,'\nget:',request.GET,'\npost:',request.POST)
        response = rspon.autoreply(request)
        return response

def access_token(request):
    access_token = query.use_access_token()
    return JsonResponse({"access_token":access_token})

def set_industry(request):
    pass

def send_model_info(request):
    content = {
        'openid':'oo9u6t9dURFOyeyHrO3m92A-s1KM',
        'template_id':'1FfIV4N0uMxCFsWadR38WdLOBAZC6xLNuKAbvcN7w7U',
        'name':'robby',
        'time':'8月6日15时46分',
    }
    response = rspon.give_model_info(content)
    url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s'%(query.use_access_token())
    res = post(url,data=response)
    print(res.json())
    return HttpResponse('success')

def setting_menu(request):
    url = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s'%(query.use_access_token())
    menu = rspon.get_menu()
    print(menu)
    res = post(url,data=menu)
    print(res.json())
    return HttpResponse('success')

def delete_menu(request):
    url = 'https://api.weixin.qq.com/cgi-bin/menu/delete?access_token=%s'%(query.use_access_token())
    res = get(url)
    print(res.json())
    return HttpResponse('success')

def enrollScholarUser(request):
    #try:
    content = request.GET.dict()
    app = App.objects.all()[0]
    openid = rspon.get_openid(app.appid,app.secret,content['code'])
    res_union = rspon.get_unionid(openid)
    collect_logger.info(str(res_union))
    divisions = divisionForm()
    context = {'openid':openid,'divisions':divisions}
    print(context)
    return render(request,'enrollScholarUser.html',context)
    '''
    except:
        return JsonResponse({'status':'fail'})
    '''

def createScholarUser(request):
    print(request.POST)
    content = request.POST.dict()
    try:
        ScholarUser.objects.get(unionCode=content['unionCode'])
        print('已注册')
        return JsonResponse({"status":'success'})
    except:
        res = query.createScholarUser(content['name'],content['tel'],content['unionCode'],query.get_division(content['section'],content['clas']))
        #发送模板消息
        mes = {
            'first':'注册信息提交成功',
            'keyword1':res.name,
            'keyword2':str(datetime.datetime.now()),
            'remark':'注册正在审核中',
            'openid':res.unionCode
        }
        model_info = rspon.send_enroll_info(mes)
        rspon.post_model_info(model_info)

        context = {}
        return render(request,'createScholarUser.html',context)

def getDivisions(request):
    if request.method == 'GET':
        return JsonResponse({'divisions':divisionForm()})
    return JsonResponse({'status':'success'})

def activate(requests,unionCode):
    user = ScholarUser.objects.get(unionCode=unionCode)
    user.activation = True
    user.save()

    #发送模板消息
    mes = {
        'first':'审核通过',
        'keyword1':user.name,
        'keyword2':str(datetime.datetime.now()),
        'remark':'恭喜您，已经成为校方审核员',
        'openid':user.unionCode
    }
    model_info = rspon.send_enroll_info(mes)
    rspon.post_model_info(model_info)
    return HttpResponseRedirect(redirect_to='/admin/public/scholaruser/')
    

