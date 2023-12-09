from django.urls import path
from django.views import View
from . import views
from django.contrib.auth import views as auth_views

app_name = 'helpdeskapp'

urlpatterns = [
    #tickets views
    path('', views.main_view, name='main_view'),
    path('ticket_list/', views.ticket_list, name='ticket_list'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('<slug:slug>/', views.ticket_detail, name='ticket_detail'),
    path('ticket/add/', views.ticket_add, name='ticket_add'),
   

    
]
