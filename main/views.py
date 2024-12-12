from django.shortcuts import render
from .models import Task

def index(request):
    return render(request, 'main/index.html')
def about(request):
    return render(request, 'main/about.html')

def trips(request):
    return render(request, 'main/trips.html')

def route(request):
    return render(request, 'main/route.html')
def budget(request):
    return render(request, 'main/budget.html')
def tasks(request):
    tasks = Task.objects.all() #.order_by()[количество]
    return render(request, 'main/tasks.html', {'tasks':tasks})
def cabinet(request):
    return render(request, 'main/cabinet.html')
