from .models import Client,Order,ServiceType,Division,Image
from django.core.files.base import ContentFile
from django.utils import timezone
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
        }

#    更改该位置
def ordersInfo(unionCode,count):
    bucket = 5
    client = Client.objects.get(unionCode=unionCode)
    orders_ = client.order.all().order_by('-id')
    length = len(orders_)
    count = int(count)
    if length>count and (length-count)%bucket!=0:
        orders = orders_[count:count+bucket]
    else:
        orders = orders_[count:]
    #order add 功能
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

def order(orderID):
    order=Order.objects.get(orderID=orderID)
    if order:
        return {
            'orderID':order.orderID,
            'client':order.client.name,
            'orderType':order.orderType,
            'technician':order.technician,
            'serviceType':order.serviceType.typ,
            'addr':order.addr,
            'model':order.model,
            'faultDescription':order.faultDescription,
            'evaluation':order.evaluation,
            'level':order.level,
            'orderStatus':order.orderStatus,
            'serviceStatus':order.serviceStatus,
            'cancel':order.cancel,
        }

def cancel(orderID):
    try:
        order = Order.objects.get(orderID=orderID)
        order.cancel = True
        order.orderStatus = '已撤销'
        order.save()
        return True
    except:
        return False

def receiveImage(img,orderID):
    image_content = ContentFile(img.read())
    image = Image(orderID=orderID,image=img)
    image.save()
