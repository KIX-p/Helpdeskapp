from django.urls import path
from . import views

app_name = 'helpdeskapp'

urlpatterns = [
    #tickets views
    path('', views.TicketListView.as_view(), name='ticket_list'),
   path('<slug:slug>/', views.ticket_detail, name='ticket_detail'),
]
