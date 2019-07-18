from django.urls import path
from . import views

app_name = 'office'
urlpatterns = [
    path('login/',views.login),
    path('enroll/',views.enroll),
    path('taskList/',views.taskList),
    path('order/',views.order)
]