from .models import VipUser,VipUserType,Level
from snack.models import Order
from django.utils import timezone
from robby.settings import BASE_HOST
from datetime import datetime
#订单日志填入
def wOrderLog(order,userType,unionCode,operation):
    orderLog = order.orderLog
    log = '——'.join((userType,unionCode,operation,str(timezone.now())))+'\n'
    orderLog += log
    order.orderLog = orderLog
    order.save()

#返回order的图片
def get_order_images(order):
    images_url = []
    images = order.img.all()
    if len(images) == 0:
        images_url = [BASE_HOST+'media/empty.jpg']
    else:
        images_url = [BASE_HOST+'media/'+str(image.image) for image in images]
    print(images_url)
    return images_url

#订单服务日志填入
def wServiceLog(order,userType,unionCode,operation):
    serviceLog = order.serviceLog
    log = '——'.join((userType,unionCode,operation,str(timezone.now())))+'\n'
    serviceLog += log
    order.serviceLog = serviceLog
    order.save()

def queryVipUser(unicode):
#查询User用户。若用户存在，返回对象，否则返回false
    try:
        return VipUser.objects.get(unionCode=unicode)
    except VipUser.DoesNotExist:
        return False

def types():
#返回用户类型
    return ['-'.join((typ.agent,typ.typ)) for typ in VipUserType.objects.all()]

#工号生成
def createJobNumber():
    return VipUser.objects.count()+1

def enroll(content):
    try:
        vipUser = VipUser.objects.get(unionCode=content['unionCode'])
        vipUser.name = content['name']
        vipUser.tel = content['tel']
        vipUser.address = content['addr']
        vipUser.save()
        return '已修改'
    except:
        agent,typ = content['vipUserType'].split('-')
        typ = VipUserType.objects.get(agent=agent,typ=typ)
        level = typ.level.get(level='初级')
        jobNumber = createJobNumber()
        #生成用户模型
        vipUser = VipUser(
            level=level,
            name=content['name'],
            tel=content['tel'],
            address=content['addr'],
            unionCode=content['unionCode'],
            jobNumber=jobNumber
            )
        vipUser.save()
        return '已注册'
#检测登录状态
def checkLogin(unionCode,code):
    return VipUser.objects.get(unionCode=unionCode).loginCode == code

#返回单个order的简要信息
def orderInfo(order):
    return {
        'serviceType':order.serviceType.typ,
        'faultDescription':order.faultDescription,
        'orderStatus':order.orderStatus,
        'serviceStatus':order.serviceStatus,
        'orderType':order.orderType,
        'orderID':order.orderID,
        'cancel':order.cancel,
        'image':get_order_images(order)[0]
        }

def ordersInfo(unionCode,count):
    bucket = 5
    vipUser = VipUser.objects.get(unionCode=unionCode)
    orders_ = vipUser.order.all().order_by('-id')
    length = len(orders_)
    count = int(count)
    if length>count and (length-count)%bucket!=0:
        orders = orders_[count:count+bucket]
    else:
        orders = orders_[count:]
    #order add 功能
    return [orderInfo(order) for order in orders]

#返回订单详情信息
def order(orderID):
    order=Order.objects.get(orderID=orderID)
    if order:
        return {
            'orderID':order.orderID,
            'client':order.client.name,
            'createTime':order.createTime,
            'orderType':order.orderType,
            'technician':order.technician.name,
            'serviceType':order.serviceType.typ,
            'addr':order.addr,
            'model':order.model,
            'faultDescription':order.faultDescription,
            'faultContent':order.faultContent,
            'costList':order.costList,
            'evaluation':order.evaluation,
            'level':order.level,
            'orderStatus':order.orderStatus,
            'serviceStatus':order.serviceStatus,
            'cancel':order.cancel,
            'images':get_order_images(order)
        }

#获取订单服务状态
def getOrderServiceStatus(serviceStatus):
    if serviceStatus == '待维修':
        return ('维修中','开始维修')
    elif serviceStatus == '维修中':
        return ('维修完成','完成维修')
    elif serviceStatus == '维修完成':
        return ('维修中','开始返修')

#订单服务状态更改
def repair(unionCode,orderID):
    order = Order.objects.get(orderID=orderID)
    serviceStatus,operation = getOrderServiceStatus(order.serviceStatus)
    order.serviceStatus = serviceStatus
    order.save()
    wServiceLog(order,'维修员',unionCode,operation)
    return order.serviceStatus

#生成费用明细
def create_cost_list(cost_list,prices):
    costList = ''
    for i in range(len(cost_list)):
        costList += cost_list[i]+'——'+prices[i]+'\n'
    return costList

#解析费用明细
def get_cost_list(orderID):
    order = Order.objects.get(orderID=orderID)
    costList = order.costList
    cost_list = []
    prices = []
    cols = costList.split('\n')
    try:
        for col in cols:  
            col_ = col.split('——')
            print(col_)
            if col_[0] == '':
                break
            cost_list.append(col_[0])
            prices.append(col_[1])
        if cost_list == []:
            cost_list.append('')
            prices.append('')
        return {'cost_list':cost_list,'prices':prices}
    except:
        return {'cost_list':cost_list,'prices':prices}

def figure_out_add_up(prices):
    res = 0
    for price in prices:
        res += float(price)
    return str(res)
def finsh_repair(unionCode,orderID,costList,prices,faultContent):
    order = Order.objects.get(orderID=orderID)
    costList_ = create_cost_list(costList,prices)
    add_up = figure_out_add_up(prices)
    serviceStatus,operation = getOrderServiceStatus(order.serviceStatus)
    order.serviceStatus = serviceStatus
    order.add_up = add_up
    order.faultContent = faultContent
    order.costList = costList_

    order.save()
    wServiceLog(order,'维修员',unionCode,operation)
    return order.serviceStatus

def get_faultContent(orderID):
    order = Order.objects.get(orderID=orderID)
    return order.faultContent

def create_job_number(vipUser):
    jobNumber = ''
    now = datetime.now()
    numbers = [now.year,now.month,now.day,vipUser.id]
    for num in numbers:
        jobNumber += str(num)
    return  jobNumber

def vipUserActivate(unionCode):
    try:
        vipUser = VipUser.objects.get(unionCode=unionCode)
        vipUser.hire = '已就职'
        vipUser.hiredate = datetime.now()
        if vipUser.hire == '审核中':
            jobNumber = create_job_number(vipUser)
            vipUser.jobNumber = jobNumber
        vipUser.save()
        return True
    except:
        return False

def vipUserDeActivate(unionCode):
    try:
        vipUser = VipUser.objects.get(unionCode=unionCode)
        vipUser.hire = '已离职'
        vipUser.dimissionTime = datetime.now()
        vipUser.save()
        return True
    except:
        return False