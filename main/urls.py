from django.contrib.auth.views import LogoutView
from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='home'),
    path('about-us/', views.about, name='about'),
    path("trips/", views.trips_view, name="trips"),
    path('route/', views.route, name='route'),
    path('budget/', views.budget_view, name='budget'),
    path('tasks/', views.tasks, name='tasks'),
    path('cabinet/', views.cabinet, name='cabinet'),
    path('registration/', views.registration, name='registration'),
    path('login/', views.login_user, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('join/<uuid:invite_code>/', views.join_trip, name='join_trip'),
    path('delete_trip/<int:id>/', views.delete_trip, name='delete_trip'),

    # Выбор путешествия
    path('trips/select/', views.select_trip, name='select_trip'),

    # Добавление пункта маршрута
    path('route/<int:route_id>/item/add/', views.add_route_item, name='add_route_item'),


    # Список пунктов маршрута
    path('route/<int:route_id>/items/', views.route_item_list, name='route_item_list'),

    # Список маршрутов для путешествия
    path('trips/routes/', views.route_list, name='route_list'),

    # Добавление маршрута в путешествие
    path('trip/<int:trip_id>/route/add/', views.add_route, name='add_route'),
    path('route/<int:route_id>/delete/', views.delete_route, name='delete_route'),
    path('route/item/<int:item_id>/edit/', views.edit_route_item, name='edit_route_item'),
    path('route/item/<int:item_id>/delete/', views.delete_route_item, name='delete_route_item'),

    path('trip/<int:trip_id>/tasks/', views.task_list, name='task_list'),
    path('trip/<int:trip_id>/tasks/create/', views.create_task, name='create_task'),

]
