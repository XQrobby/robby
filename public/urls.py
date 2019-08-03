from django.urls import path
from . import views

app_name = 'public'
urlpatterns = [
    path('',views.wechat,name='wechat'),
    path('develop/',views.develop,name='develop')
]
