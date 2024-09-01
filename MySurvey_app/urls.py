from django.urls import path
from . import views

urlpatterns = [
    path('', views.log_and_reg, name='log_and_reg'),
    path('index', views.index, name='index'),
    path('process', views.process, name='process'),
    path('result', views.result, name='result'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
]
