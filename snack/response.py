from json import dumps
from requests import post
from public.dateBaseQuery import use_access_token
from .dateBaseQuery import query_public_unionCode

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
def enroll_create(content):
    #client、enrollTime
    response = {
        "touser":content['unionCode'],
        "template_id":'fmuMocp62Fpufwjqgt6p33z54QlD1N2JFtdN_reUAEg',
        "topcolor":"#FF0000",
        "data":{
            "first":{
                "value":'用户注册成功',
                "color":"#173177"
            },
            "keyword1":{
                "value":content['client'],
                "color":"#173177"
            },
            "keyword2":{
                "value":content['enrollTime'],
                "color":"#173177"
            },
            "remark":{
                "value":'感谢注册',
                "color":"#173177"
            }
        }
    }
    return dumps(response)
#下单成功
#个人订单
def put_order_person_create(content):
    #orderID、section、model、createTime
    response = {
        "touser":content['unionCode'],
        "template_id":'XIRUpvOYl1iXN7Ykq9k4JL0OoSgxCa3SUQm88X7lYWM',
        "topcolor":"#FF0000",
        "data":{
            "first":{
                "value":'下单成功',
                "color":"#173177"
            },
            "keyword1":{
                "value":content['orderID'],
                "color":"#173177"
            },
            "keyword2":{
                "value":content['section'],
                "color":"#173177"
            },
            "keyword3":{
                "value":content['model'],
                "color":"#173177"
            },
            "keyword4":{
                "value":content['createTime'],
                "color":"#173177"
            },
            "remark":{
                "value":'您可以在公众号发送消息与客服联系',
                "color":"#173177"
            }
        }
    }
    return dumps(response)
#学校订单
def put_order_scholar_create(content):
    #信息serviceType、section、clas、client、tel
    response = {
        "touser":content['unionCode'],
        "template_id":'yaChVhy5hzr3AY3lIhLKnVx9bC-MN3-VtPXcLaDtPy0',
        "topcolor":"#FF0000",
        "data":{
            "first":{
                "value":'下单成功',
                "color":"#173177"
            },
            "keyword1":{
                "value":content['serviceType'],
                "color":"#173177"
            },
            "keyword2":{
                "value":content['section'],
                "color":"#173177"
            },
            "keyword3":{
                "value":content['clas'],
                "color":"#173177"
            },
            "keyword4":{
                "value":content['client'],
                "color":"#173177"
            },   
            "keyword5":{
                "value":content['tel'],
                "color":"#173177"
            },          
            "remark":{
                "value":'您可以在公众号发送消息与客服联系',
                "color":"#173177"
            }
        }
    }
    return dumps(response)
#订单已下派
def arrange_order_create(content):
    #信息tech、tel、bookingTime、model、faultDescription
    response = {
        "touser":content['unionCode'],
        "template_id":'HBpBHWieF8HzKddJJeBv_W8Bs_rVpQka7g2aolF0P0g',
        "topcolor":"#FF0000",
        "data":{
            "first":{
                "value":'维修申请已派单',
                "color":"#173177"
            },
            "keyword1":{
                "value":content['tech'],
                "color":"#173177"
            },
            "keyword2":{
                "value":content['tel'],
                "color":"#173177"
            },
            "keyword3":{
                "value":content['bookingTime'],
                "color":"#173177"
            },
            "keyword4":{
                "value":content['model'],
                "color":"#173177"
            },
            "keyword5":{
                "value":content['faultDescription'],
                "color":"#173177"
            },
            "remark":{
                "value":'请耐心等待',
                "color":"#173177"
            }
        }
    }
    return dumps(response)
#维修完成
def finish_order_create(content):
    #tech、tel、finishTime
    response = {
        "touser":content['unionCode'],
        "template_id":'gey7ZccA91bj0H5K_rnu0eg33g8Rvy8gpmR5FrbNikE',
        "topcolor":"#FF0000",
        "data":{
            "first":{
                "value":'订单已完修',
                "color":"#173177"
            },
            "keyword1":{
                "value":content['tech'],
                "color":"#173177"
            },
            "keyword2":{
                "value":content['tel'],
                "color":"#173177"
            },
            "keyword3":{
                "value":content['finishTime'],
                "color":"#173177"
            },
            "keyword4":{
                "value":'订单维修完成',
                "color":"#173177"
            },
            "remark":{
                "value":'更多信息见微信小程序，也可以通过微信公众号咨询客服',
                "color":"#173177"
            }
        }
    }
    return dumps(response)

def send_model_info(content,model_info_create):
    #content必需包含openid，并包含相应模板所需的数据
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
    unionCode_ = query_public_unionCode(content['unionCode'])
    content['unionCode'] = unionCode_
    model_info = model_info_create(content)
    url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s'%(use_access_token())
    res = post(url,data=model_info)
    print(res.json())
    return res.json()