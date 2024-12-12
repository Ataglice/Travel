from django.urls import path

from main.urls import urlpatterns
from . import views

urlpatterns = [
    path('trips/', views.trip_list, name='trip-list'),
    path('trips/<int:trip_id>/', views.trip_detail, name='trip-detail'),
    path('trip-members/', views.trip_member_list, name='trip-member-list'),
    path('tasks/', views.task_list, name='task-list'),
    path('expenses/', views.expense_list, name='expense-list'),
    path('messages/', views.message_list, name='message-list'),
    path('login/', views.LoginView.as_view(), name='login'),
]