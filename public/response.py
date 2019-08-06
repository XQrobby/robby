from wechatpy import parse_message,create_reply
from django.http.response import HttpResponse,JsonResponse
from json import dumps
def autoreply(request):
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

def give_model_info(content):
    response = {
        "touser":content['openid'],
        "template_id":content['template_id'],
        "topcolor":"#FF0000",
        "data":{
            "name":{
                "value":content['name'],
                "color":"#173177"
            },
            "time":{
                "value":content['time'],
                "color":"#173177"
            }
        }
    }
    return dumps(response)

def get_menu():
    response = {
        "button":[
            {
                "type":"view",
                "name":"Biao维修",
                "url":"http://120.27.242.55/admin/"
            },
            {
                "name":"管理员入口",
                "sub_button":[
                    {
                        "type":"view",
                        "name":"订单管理",
                        "url":"http://120.27.242.55/admin/"
                    },
                    {
                        "type":"view",
                        "name":"成为校方审核员",
                        "url":"http://www.baidu.com/"
                    }
                ]
            }
        ]
    }
    return dumps(response)