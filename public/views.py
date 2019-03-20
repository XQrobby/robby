from django.shortcuts import render
from django.http.response import HttpResponse
from wechatpy import parse_message,create_reply
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.utils import check_signature

# Create your views here.
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
        response = HttpResponse(reply.render(),context_type='application/xml')
        return response
    else:
        logger.info('-----------------')    