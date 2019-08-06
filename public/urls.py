from django.urls import path
from . import views

app_name = 'public'
urlpatterns = [
    #path('',views.wechat,name='wechat'),
    path('develop/',views.develop,name='develop'),
    path('access_token/',views.access_token,name='access_token'),
    path('set_access_token/',views.set_industry,name='set_industry'),
    path('send_model_info/',views.send_model_info,name='send_model_info'),
]
