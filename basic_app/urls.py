from django.contrib import admin
from django.urls import path
from basic_app import views
from django.conf.urls import url


#  TEMPLATE tagging
app_name = 'basic_app'

urlpatterns = [
    url(r'^$', views.index,name = 'index'),
    # url(r'^emotions/$', views.emotions,name = 'emotions'),
    url(r'^emotions_form/$', views.emotions_form,name = 'emotions_form'),

    url(r'^login/$', views.login,name = 'login'),
    url(r'^signup/$', views.signup,name = 'signup'),
    url(r'^vis/$', views.vis,name = 'vis'),
    url(r'^emotions/$', views.emotions,name = 'emotions'),
    url(r'^stocks/$', views.stocks,name = 'stocks'),
    url(r'^add_stock/$', views.add_stock,name = 'add_stock'),

]

