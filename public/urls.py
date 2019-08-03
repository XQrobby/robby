from django.urls import path
from . import views

app_name = 'public'
urlpatterns = [
    path('',views.wechat,name='wechat'),
    path('develop/',views.develop,name='develop'),
    path('access_token/',views.access_token,name='access_token'),
]
