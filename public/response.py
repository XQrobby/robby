from wechatpy import parse_message,create_reply
from django.http.response import HttpResponse,JsonResponse

def autoreply(request):
    try:
        print(request.body)
        msg = parse_message(request.body)
        if msg.type == 'text':
            reply = create_reply('这是条文字消息',msg)
            print('这是条文字消息')
        elif msg.type == 'image':
            reply = create_reply('这是条图片消息',msg)
            print('这是条图片消息')
        elif msg.type == 'voice':
            reply = create_reply('这是条语音消息',msg)
            print('这是条语音消息')
        else:
            reply = create_reply('这是条其他类型消息',msg)
            print('这是条其他类型消息')
        #response = HttpResponse(reply.render(),content_type='application/xml')
        #return response
    except:
        reply = create_reply('---------',msg)  
        #response = HttpResponse(reply.render(),content_type='application/xml')
        #return response