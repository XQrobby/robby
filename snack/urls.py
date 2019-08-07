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
    path('assess_id=<int:order_id>/',views.assess,name='assess'),
    path('choiceTech/',views.choiceTech,name='choiceTech'),
    path('finish_id=<int:order_id>/',views.finish,name='finish'),
    path('affirm_finish/',views.affirm,name='affirm'),
    path('photo=<int:order_id>/',views.photo,name='photo'),
    path('orderCheck/',views.orderCheck,name='orderCheck'),
]