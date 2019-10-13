from json import dumps
from requests import post
from public.dateBaseQuery import use_access_token
from .dateBaseQuery import query_publicUnionCode_with_vipUser_unionCode

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
#注册成功，等待审核
def enroll_success_create(content):
    #name、enrollTime
    response = {
        "touser":content['unionCode'],
        "template_id":'fmuMocp62Fpufwjqgt6p33z54QlD1N2JFtdN_reUAEg',
        "topcolor":"#FF0000",
        "data":{
            "first":{
                "value":'维修员注册成功',
                "color":"#173177"
            },
            "keyword1":{
                "value":content['name'],
                "color":"#173177"
            },
            "keyword2":{
                "value":content['enrollTime'],
                "color":"#173177"
            },
            "remark":{
                "value":'等待审核员审核',
                "color":"#173177"
            }
        }
    }
    return dumps(response)
#审核通过
def enroll_check_create(content):
    #name、hiredate
    response = {
        "touser":content['unionCode'],
        "template_id":'fmuMocp62Fpufwjqgt6p33z54QlD1N2JFtdN_reUAEg',
        "topcolor":"#FF0000",
        "data":{
            "first":{
                "value":'维修员资格审核通过',
                "color":"#173177"
            },
            "keyword1":{
                "value":content['name'],
                "color":"#173177"
            },
            "keyword2":{
                "value":content['hiredate'],
                "color":"#173177"
            },
            "remark":{
                "value":'感谢注册',
                "color":"#173177"
            }
        }
    }
    return dumps(response)
#有新的订单
def new_task_create(content):
    #orderID、section_clas、model、time
    response = {
        "touser":content['unionCode'],
        "template_id":'XIRUpvOYl1iXN7Ykq9k4JL0OoSgxCa3SUQm88X7lYWM',
        "topcolor":"#FF0000",
        "data":{
            "first":{
                "value":'您有新的维修任务',
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
                "value":'详情请在微信小程序查询',
                "color":"#173177"
            }
        }
    }
    return dumps(response)

def dismission_create(content):
    #name、dimissionTime
    response = {
        "touser":content['unionCode'],
        "template_id":'fmuMocp62Fpufwjqgt6p33z54QlD1N2JFtdN_reUAEg',
        "topcolor":"#FF0000",
        "data":{
            "first":{
                "value":'维修员已离职',
                "color":"#173177"
            },
            "keyword1":{
                "value":content['name'],
                "color":"#173177"
            },
            "keyword2":{
                "value":content['dimissionTime'],
                "color":"#173177"
            },
            "remark":{
                "value":'请与管理员核实',
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
    unionCode_ = query_publicUnionCode_with_vipUser_unionCode(content['unionCode'])
    content['unionCode'] = unionCode_
    model_info = model_info_create(content)
    url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s'%(use_access_token())
    res = post(url,data=model_info)
    print(res.json())
    return res.json()