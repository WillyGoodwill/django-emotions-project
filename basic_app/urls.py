from django.contrib import admin
from django.urls import path
from basic_app import views
from django.conf.urls import url


#  TEMPLATE taggingh
app_name = 'basic_app'
urlpatterns = [
    url(r'^$', views.index,name = 'index'),
    url(r'^emotions/$', views.emotions,name = 'emotions'),
]

