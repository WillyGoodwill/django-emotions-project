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

    # url(r'^login/$', views.login,name = 'login'),
    path('logout/', views.logoutuser,name = 'logoutuser'),
    path('login/', views.loginuser,name = 'loginuser'),
    path('signup/', views.signupuser,name = 'signup'),
    url(r'^vis/$', views.vis,name = 'vis'),
    url(r'^emotions/$', views.emotions,name = 'emotions'),
    url(r'^stocks/$', views.stocks,name = 'stocks'),
    url(r'^add_stock/$', views.add_stock,name = 'add_stock'),
    url(r'^delete/<stock_id>$', views.delete,name = 'delete'),
    url(r'^test_about_me/$', views.about_me,name = 'about_me'),
    path('delete_about_me/<int:text_id>', views.delete_about_me,name = 'delete_about_me'),
    path('delete_about_me_others/<int:text_id>', views.delete_about_me_others,name = 'delete_about_me_others'),
    path('delete_about_me_future/<int:text_id>', views.delete_about_me_future,name = 'delete_about_me_future')

]

