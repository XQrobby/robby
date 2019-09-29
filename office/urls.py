from django.urls import path
from . import views

app_name = 'office'
urlpatterns = [
    path('login/',views.login),
    path('enroll/',views.enroll),
    path('taskList/',views.taskList),
    path('order/',views.order),
    path('repair/',views.repair),
    path('finshRepair/',views.finshRepair),
    path('complete/',views.complete),
    path('activate_unionCode=<str:unionCode>/',views.activate),
    path('deactivate_unionCode=<str:unionCode>/',views.deactivate),
    path('activate_opt/',views.activate_opt,name='activate_opt'),
    path('deactivate_opt/',views.deactivate_opt,name='deactivate_opt'),
]