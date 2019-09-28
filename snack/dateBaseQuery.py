from .models import Client,Order,ServiceType,Division,Image
from office.models import VipUser
from django.core.files.base import ContentFile
from django.utils import timezone
from office.dateBaseQuery import wOrderLog,wServiceLog
from robby.settings import BASE_HOST
def queryClient(unicode):
#查询User用户。若用户存在，返回对象，否则返回false
    try:
        return Client.objects.get(unionCode=unicode)
    except Client.DoesNotExist:
        return False

def clientDetail(client):
#查询User用户的详情信息
    return  {
        'name':client.name,
        'tel':client.tel,
        'unionCode':client.unionCode,
        'clientID':client.clientID,
        'section':client.section,
        'clas':client.clas,
        'addrs':client.addrs.split(',')
    }

#user初始化
def clientInit(unionCode):
    client = Client(unionCode=unionCode)
    client.save()
    return client

#检测登录状态
def checkLogin(unionCode,code):
    return Client.objects.get(unionCode=unionCode).loginCode == code
    

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

#    更改该位置
def ordersInfo(unionCode,count):
    bucket = 5
    client = Client.objects.get(unionCode=unionCode)
    orders_ = client.order.all().order_by('-id')
    length = len(orders_)
    count = int(count)
    orders = []
    '''
    if length>count and (length-count)%bucket!=0:
        orders = orders_[count:count+bucket]
    else:
        orders = orders_[count:]
    '''
    try:
        orders = orders_[count:count+bucket]
    except:
        orders = orders_[count:]
    #order add 功能
    print(orders,orders_)
    return [orderInfo(order) for order in orders]

def changeClientInfo(content):
    client = Client.objects.get(unionCode=content['unionCode'])
    client.name = content['name']
    client.tel = content['tel']
    client.clas = content['clas']
    client.section = content['section']
    client.addrs = content['addrs']
    client.save()


def createOrder(content):
    order = Order(
        client = Client.objects.get(unionCode=content['unionCode']),
        serviceType = ServiceType.objects.get(typ=content['serviceType']),
        model = content['model'],
        faultDescription = content['faultDescription'],
        addr = content['addr'],
        orderType = '个人订单',
    )
    order.save()
    wOrderLog(order,'普通用户',content['unionCode'],'创建订单')
    return order

def createScholarOrder(content):
    order = Order(
            client = Client.objects.get(unionCode=content['unionCode']),
            serviceType = ServiceType.objects.get(typ=content['serviceType']),
            model = content['model'],
            faultDescription = content['faultDescription'],
            addr = content['addr'],
            division = Division.objects.get(section=content['section'],clas=content['clas']),
            orderType = '学校订单',
        )
    order.save()
    wOrderLog(order,'普通用户',content['unionCode'],'创建订单')
    return order


def makeOrderId(newOrder):
    time = timezone.now()
    newOrder.orderID = str(time.year)[2:]+str(time.month)+str(time.day)+str(newOrder.id)
    newOrder.save()
    return newOrder.orderID

def nOrder(content):
    if content['orderType'] == '个人订单':  
        orderID = makeOrderId(createOrder(content))
    elif content['orderType'] == '学校订单':
        orderID = makeOrderId(createScholarOrder(content))
    return orderID


def divisionForm():
    sections = set([division.section for division in Division.objects.all()])
    return {section:[division.clas for division in Division.objects.filter(section=section)] for section in sections}

def serviceTypeForm():
    return [ serviceType.typ for serviceType in ServiceType.objects.all() ]
#后去order图片
def get_order_images(order):
    images_url = []
    images = order.img.all()
    if len(images) == 0:
        images_url = [BASE_HOST+'media/empty.jpg']
    else:
        images_url = [BASE_HOST+'media/'+str(image.image) for image in images]
    print(images_url)
    return images_url
def order(orderID):
    order=Order.objects.get(orderID=orderID)
    if order:
        order_info = {
            'orderID':order.orderID,
            'client':order.client.name,
            'orderType':order.orderType,
            'serviceType':order.serviceType.typ,
            'addr':order.addr,
            'model':order.model,
            'faultDescription':order.faultDescription,
            'evaluation':order.evaluation,
            'level':order.level,
            'orderStatus':order.orderStatus,
            'serviceStatus':order.serviceStatus,
            'cancel':order.cancel,
            'costList':order.costList,
            'images':get_order_images(order),
        }
        if order.orderStatus != '审核中' and order.orderStatus != '已撤销':
            order_info['technician'] = order.technician.name
        return order_info

def cancel(orderID,unionCode):
    try:
        order = Order.objects.get(orderID=orderID)
        order.cancel = True
        order.orderStatus = '已撤销'
        order.save()
        wOrderLog(order,'普通用户',unionCode,'取消订单')
        return True
    except:
        return False

def receiveImage(img,orderID):
    order = Order.objects.get(orderID=orderID)
    image_content = ContentFile(img.read())
    image = Image(orderID=orderID,image=img)
    image.order = order
    image.save()

def setTech(content):
    order = Order.objects.get(id=content['order_id'])
    tech = VipUser.objects.get(id=content['tech_id'])
    order.technician = tech
    order.orderStatus = '等待维修'
    order.serviceStatus = '待维修'
    order.is_assess = True
    order.save()
    wOrderLog(order,'调度员',content['user_id'],'下派订单-->'+tech.name)
    wServiceLog(order,'调度员',content['user_id'],'下派订单-->'+tech.name)

def affirmFinish(content):
    order = Order.objects.get(id=content['order_id'])
    order.orderStatus = '已完修'
    order.costList = content['costList']
    order.save()
    wOrderLog(order,'调度员',content['user_id'],'订单完修')

def checkLevel(level):
    if level == '':
        return '无'
    else:
        return level

def orderCheck(content):
    try:
        level = checkLevel(content['level'])
        order = Order.objects.get(orderID=content['orderID'])
        order.level = level
        order.evaluation = content['evaluation']
        if order.orderStatus == '已完修':
            order.orderStatus = '已验收'
        order.save()
        wOrderLog(order,'普通用户',content['unionCode'],'订单完修')
        return True
    except Exception as e:
        print(e)
        return '验收未成功，请稍后重试'
