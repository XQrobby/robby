from .models import AssessToken,App,ScholarUser,Agency
from snack.models import Division,Order
import datetime
from requests import request,get
import logging
collect_logger = logging.getLogger('scripts')
#从数据库查询access_token对象
def query_access_token():
    return AssessToken.objects.all()[0]

#保存access_token
def save_access_token(access_token):
    save_time = datetime.datetime.now()
    data_line = save_time + datetime.timedelta(seconds=6950)
    try:
        token = query_access_token()
        token.access_token = access_token
        token.save_time = save_time
        token.data_line = data_line
    except:
        token = AssessToken(access_token=access_token,save_time=save_time,data_line=data_line)
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

def use_access_token():
    token = ''
    try:
        access_token = query_access_token()
        #验证access_token的有效性
        if check_assessToken(access_token):
            token = access_token.access_token
            return token
        else:
            #access_token无效，重新获取access_token
            access_token = get_access_token()
            return access_token.access_token
            
    except:
        #access_token不存在，对access_token进行初始化
        get_access_token()
        access_token = query_access_token()
        return access_token.access_token 
    
def createScholarUser(name,tel,unionCode,division):
    newUser = ScholarUser(
        name = name,
        tel = tel,
        unionCode = unionCode,
        division = division
    )
    newUser.save()
    return newUser

def get_division(section,clas):
    return Division.objects.get(section=section,clas=clas)

def check_scholar_user(unionCode):
    try:
        user = ScholarUser.objects.get(unionCode=unionCode)
        return False
    except:
        return True

def check_agency(unionCode):
    try:
        agency = Agency.objects.get(unionCode=unionCode)
        return False
    except:
        return True

def get_unionid(openid):
    url = 'https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s&lang=zh_CN'%(use_access_token(),openid)
    res = get(url)
    if res.status_code == 200:
        data = res.json()
        if data['unionid']:
            return {'status':True,'unionid':data['unionid']}
    return {'status':False,'unionid':''}

def createAgency(unionCode):
    if check_agency(unionCode):
        res_unionID = get_unionid(unionCode)
        agency = Agency(unionCode=unionCode,unionID=res_unionID['unionid'])
        agency.save()
        collect_logger.info('unionCode:%s\nunionid:%s'%(agency.unionID,agency.unionID))
        return True
    else:
        return False

def deleteAgency(unionCode):
    try:
        agency = Agency.objects.get(unionCode=unionCode)
        agency.delete()
        return True
    except:
        return False

def query_unionCode_by_unionID(unionID):
    agency = Agency.objects.get(unionID=unionID)
    return agency.unionCode

def checkScholarOrder(orderID,unionCode):
    order = Order.obejcts.get(orderID=orderID)
    user = ScholarUser.objects.get(unionCode=unionCode)
    if order.division == user.division:
        order.audit = True
        return True
    return False