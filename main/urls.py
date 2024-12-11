from setuptools.extern import names

from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='home'),
    path('about-us', views.about, name='about'),
    path('trips', views.trips, name='trips'),
    path('route', views.route, name='route'),
    path('budget', views.budget, name='budget'),
    path('tasks', views.tasks, name='tasks'),
    path('cabinet', views.cabinet, name='cabinet'),
]