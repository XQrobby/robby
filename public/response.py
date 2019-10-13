from wechatpy import parse_message,create_reply
from django.http.response import HttpResponse,JsonResponse
from .models import App
from requests import get,post
from json import dumps
from .dateBaseQuery import use_access_token,createAgency,deleteAgency
from json import dumps

def autoreply(request):
    msg = parse_message(request.body)
    reply = create_reply('',msg)
    print("type:",msg.type,"\n",dir(msg))
    if msg.type == 'text':
        reply = create_reply('这是条文字消息', msg)
    elif msg.type == 'image':
        reply = create_reply('这是条图片消息', msg)
    elif msg.type == 'voice':
        reply = create_reply('这是条语音消息', msg)
    elif msg.type == 'event':
        if msg.event == 'subscribe':
            reply = create_reply('感谢关注',msg)
            res = createAgency(request.GET.get('openid'))
        elif msg.event == 'unsubscribe':
            res = deleteAgency(request.GET.get('openid'))
    else:
        reply = create_reply('这是条其他类型消息', msg)
    response = HttpResponse(reply.render(), content_type="application/xml")
    return response

def get_menu():
    app = App.objects.all()[0]
    response = {
        "button":[
            {
                "type":"view",
                "name":"Beao维修",
                "url":"https://120.27.242.55/admin/"
            },
            {
                "name":"管理员入口",
                "sub_button":[
                    {
                        "type":"view",
                        "name":"订单管理",
                        "url":"https://120.27.242.55/admin/"
                    },
                    {
                        "type":"view",
                        "name":"成为校方审核员",
                        "url":"https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=https://www.robbyzhang.cn/public/enrollScholarUser/&response_type=code&scope=snsapi_base&state=STATE#wechat_redirect"%(app.appid)
                    }
                ]
            }
        ]
    }
    return dumps(response,ensure_ascii=False).encode("utf-8")

def get_openid(appid,secret,code):
    url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code'%(appid,secret,code)
    res = get(url)
    res = res.json()
    print(res)
    return res.get('openid')

def send_enroll_info(content):
    #返回用户注册模板信息
    response = {
        "touser":content['unionCode'],
        "template_id":'fmuMocp62Fpufwjqgt6p33z54QlD1N2JFtdN_reUAEg',
        "topcolor":"#FF0000",
        "data":{
            "first":{
                "value":content['first'],
                "color":"#173177"
            },
            "keyword1":{
                "value":content['keyword1'],
                "color":"#173177"
            },
            "keyword2":{
                "value":content['keyword2'],
                "color":"#173177"
            },
            "remark":{
                "value":content['remark'],
                "color":"#173177"
            }
        }
    }
    return dumps(response)

def post_model_info(model_info):
    url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s'%(use_access_token())
    res = post(url,data=model_info)
    print(res.json())

def get_unionid(openid):
    url = 'https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s&lang=zh_CN'%(use_access_token(),openid)
    res = get(url)
    if res.status_code == 200:
        data = res.json()
        if data['unionid']:
            return {'status':True,'unionid':data['unionid']}
    return {'status':False,'unionid':''}
'''
#返回用户注册模板信息
response = {
    "touser":content['unionCode'],
    "template_id":'fmuMocp62Fpufwjqgt6p33z54QlD1N2JFtdN_reUAEg',
    "topcolor":"#FF0000",
    "data":{
        "first":{
            "value":content['first'],
            "color":"#173177"
        },
        "keyword1":{
            "value":content['keyword1'],
            "color":"#173177"
        },
        "keyword2":{
            "value":content['keyword2'],
            "color":"#173177"
        },
        "remark":{
            "value":content['remark'],
            "color":"#173177"
        }
    }
}
return dumps(response)
'''
#注册成功
def enroll_success_create(content):
    #name、time
    response = {
        "touser":content['unionCode'],
        "template_id":'fmuMocp62Fpufwjqgt6p33z54QlD1N2JFtdN_reUAEg',
        "topcolor":"#FF0000",
        "data":{
            "first":{
                "value":'注册信息提交成功',
                "color":"#173177"
            },
            "keyword1":{
                "value":content['name'],
                "color":"#173177"
            },
            "keyword2":{
                "value":content['time'],
                "color":"#173177"
            },
            "remark":{
                "value":'注册正在审核中',
                "color":"#173177"
            }
        }
    }
    return dumps(response)

#审核通过
def check_success_create(content):
    #name、time
    response = {
        "touser":content['unionCode'],
        "template_id":'fmuMocp62Fpufwjqgt6p33z54QlD1N2JFtdN_reUAEg',
        "topcolor":"#FF0000",
        "data":{
            "first":{
                "value":'审核通过',
                "color":"#173177"
            },
            "keyword1":{
                "value":content['name'],
                "color":"#173177"
            },
            "keyword2":{
                "value":content['time'],
                "color":"#173177"
            },
            "remark":{
                "value":'恭喜您，已经成为校方审核员',
                "color":"#173177"
            }
        }
    }
    return dumps(response)

#新的订单审核
def scholar_check_create(content):
    #orderID、section_clas、model、time
    response = {
        "touser":content['unionCode'],
        "template_id":'XIRUpvOYl1iXN7Ykq9k4JL0OoSgxCa3SUQm88X7lYWM',
        "url":"https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=https://www.robbyzhang.cn/public/orderCheck_orderID=%s/&response_type=code&scope=snsapi_base&state=STATE#wechat_redirect"%(app.appid,content['orderID']),
        "topcolor":"#FF0000",
        "data":{
            "first":{
                "value":'新的学院维修订单',
                "color":"#173177"
            },
            "keyword1":{
                "value":content['orderID'],
                "color":"#173177"
            },
            "keyword2":{
                "value":content['section_clas'],
                "color":"#173177"
            },
            "keyword3":{
                "value":content['model'],
                "color":"#173177"
            },
            "keyword4":{
                "value":content['time'],
                "color":"#173177"
            },
            "remark":{
                "value":'点击详情审核订单',
                "color":"#173177"
            }
        }
    }
    return dumps(response)


def send_model_info(content,model_info_create):
    #content必需包含openid、template_id，并包含相应模板所需的数据
    '''
    model_info_create为模板消息构建函数,所有的模板消息构建函数函数名都必须以_create结尾
    
    ### 模板消息构建函数使用方法 ###
        model_info_create(content)
    
    ### 模板消息构建函数格式 ###
        def model_info_create(content):
            msg = {
                'touser':content.get('unionCode') #使用get方法避免报错
            }
            return dumps(msg)
    '''
    model_info = model_info_create(content)
    url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s'%(use_access_token())
    res = post(url,data=model_info)
    print(res.json())
    return res.json()