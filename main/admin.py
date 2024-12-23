from django.contrib import admin
from .models import Category, RouteItem, Vote
from .models import Task
admin.site.register(Task)
admin.site.register(Category)
admin.site.register(RouteItem)
admin.site.register(Vote)