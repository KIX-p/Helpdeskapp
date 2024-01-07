from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('ticket/detail/<slug:slug>/chat', views.chat_room, name='chat_room'),
]