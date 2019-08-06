from django.shortcuts import render
from django.http.response import HttpResponse,JsonResponse
from wechatpy import parse_message,create_reply
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.utils import check_signature
import public.dateBaseQuery as query
import hashlib
import public.response as rspon
from requests import post

# Create your views here.
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
        print(request.body)
        msg = parse_message(request.body)
        if msg.type == 'text':
            reply = create_reply('这是条文字消息', msg)
        elif msg.type == 'image':
            reply = create_reply('这是条图片消息', msg)
        elif msg.type == 'voice':
            reply = create_reply('这是条语音消息', msg)
        else:
            reply = create_reply('这是条其他类型消息', msg)
        response = HttpResponse(reply.render(), content_type="application/xml")
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
    res = post(url,json=response)
    print(res.json)
    return HttpResponse('success')
    

