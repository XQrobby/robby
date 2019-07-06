from django.urls import path
from . import views

app_name = 'snack'
urlpatterns = [
    path('login/',views.login),
    path('changeClientInfo/',views.changeClientInfo),
    path('newOrder/',views.newOrder),
    path('orderPic/',views.orderPic),
    path('orderList/',views.orderList),
    path('order/',views.order),
    path('cancel/',views.cancel),
]