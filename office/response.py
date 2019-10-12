from json import dumps
from requests import post
from public.dateBaseQuery import use_access_token

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
#有新的订单

#订单完修

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