from django.urls import path
from . import views

app_name = 'public'
urlpatterns = [
    #path('',views.wechat,name='wechat'),
    path('develop/',views.develop,name='develop'),
    path('access_token/',views.access_token,name='access_token'),
    path('set_access_token/',views.set_industry,name='set_industry'),
    path('send_model_info/',views.send_model_info,name='send_model_info'),
    path('setting_menu/',views.setting_menu,name='setting_menu'),
    path('delete_menu/',views.delete_menu,name="delete_menu"),
    path('enrollScholarUser/',views.enrollScholarUser,name='enrollScholarUser'),
    path('createScholarUser/',views.createScholarUser,name='createScholarUser'),
    path('getDivisions/',views.getDivisions,name='getDivisions'),
    path('activate_unionCode=<str:unionCode>/',views.activate,name='activate'),
    path('orderCheck_orderID=<str:orderID>/',views.orderCheck,name='orderCheck_scholar')
]
