from .models import AssessToken,App
import datetime
from requests import request

#保存access_token
def save_access_token(access_token):
    save_time = datetime.datetime.now()
    data_line = save_time + datetime.timedelta(seconds=6950)
    try:
        token = AssessToken.objects.all()[0]
        token.access_token = access_token
        token.save_time = save_time
        token.data_line = data_line
    except:
        token = AssessToken(access_token=access_token,save_time=save_time,datetime=data_line)
    token.save()

#检验access_token的有效性,有效返回True
def check_assessToken(token):
    now = datetime.datetime.now()
    return now < token.data_line

#获取access_token
def get_access_token():
    app = App.objects.all()[0]
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s'%(app.appid,app.secret)
    r = request('GET',url)
    res = r.json()
    save_access_token(res['access_token'])

def usr_access_token():
    pass

