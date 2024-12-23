from .models import Task, TripMember, Route, RouteVote
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Trip
from urllib.parse import urljoin
from .models import RouteItem, Category, Vote
from .forms import RouteItemForm, RouteForm, TaskForm


def index(request):
    return render(request, 'main/index.html')
def about(request):
    return render(request, 'main/about.html')

def trips(request):
    return render(request, 'main/trips.html')


def budget(request):
    return render(request, 'main/budget.html')
def tasks(request):
    tasks = Task.objects.all() #.order_by()[количество]
    return render(request, 'main/tasks.html', {'tasks':tasks})
def cabinet(request):
    return render(request, 'main/cabinet.html')



def registration(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember-me')

        if not email or not username or not password:
            messages.error(request, "Заполни поля!")
            return render(request, 'auth/registration.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Пользователь уже существует!")
            return render(request, 'auth/registration.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Почта уже существует!")
            return render(request, 'auth/registration.html')

        # Создание пользователя
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        # Аутентификация пользователя сразу после регистрации
        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)

            # Устанавливаем длительность сессии, если "Remember me" отмечен
            if remember_me:
                request.session.set_expiry(1209600)  # 2 недели
            else:
                request.session.set_expiry(0)  # Закрыть сессию при закрытии браузера

            messages.success(request, "Registration successful!")
            return redirect('cabinet')  # Перенаправляем на главную страницу
        else:
            messages.error(request, "Authentication failed!")

    return render(request, 'auth/registration.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)  # Входим пользователя в сессию
            return redirect('cabinet')  # Перенаправление на главную страницу
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'auth/login.html')




@login_required
def cabinet(request):
    return render(request, 'main/cabinet.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def trips_view(request):
    if request.method == "POST":
        name = request.POST["name"]
        start_date = request.POST["start_date"]
        end_date = request.POST["end_date"]
        destination = request.POST["destination"]

        # Создание путешествия
        trip = Trip.objects.create(
            name=name,
            start_date=start_date,
            end_date=end_date,
            destination=destination,
            created_by=request.user,
        )
        # Добавление создателя в участники
        TripMember.objects.create(trip=trip, user=request.user, role='admin')
        return redirect("trips")

    # Отображение списка путешествий
    trips = Trip.objects.filter(members__user=request.user).distinct()

    # Добавляем ссылки приглашений
    for trip in trips:
        trip.invite_link = urljoin(request.build_absolute_uri('/'), trip.invite_url())

    return render(request, "main/trips.html", {"trips": trips})

def join_trip(request, invite_code):
    trip = get_object_or_404(Trip, invite_code=invite_code)
    if request.user.is_authenticated:
        # Проверяем, если пользователь уже участник или является создателем
        if not TripMember.objects.filter(trip=trip, user=request.user).exists() and trip.created_by != request.user:
            TripMember.objects.create(trip=trip, user=request.user, role='member')
        return redirect("trips")
    return redirect("login")

@login_required
def delete_trip(request, id):
    if request.method == 'POST':
        try:
            trip = Trip.objects.get(id=id)
            # Проверка: пользователь должен быть создателем путешествия
            if trip.created_by == request.user:
                trip.delete()
            else:
                return HttpResponseForbidden("Вы не можете удалить это путешествие, так как вы не являетесь его создателем.")
        except Trip.DoesNotExist:
            pass
    return redirect('trips')

@login_required
def add_route(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)

    if trip.created_by != request.user:
        messages.error(request, "У вас нет прав добавлять маршруты для этого путешествия.")
        return redirect('route_list')  # Перенаправление на список маршрутов

    if request.method == "POST":
        form = RouteForm(request.POST)
        if form.is_valid():
            route = form.save(commit=False)
            route.trip = trip
            route.save()
            return redirect('route_list')
    else:
        form = RouteForm()
    return render(request, 'main/add_route.html', {'form': form, 'trip': trip})

@login_required
def route_item_list(request, route_id):
    route = get_object_or_404(Route, id=route_id)

    # Проверка: только администратор путешествия может видеть пункты маршрута
    if route.trip.created_by != request.user:
        return HttpResponseForbidden("Вы не можете просматривать пункты этого маршрута.")

    items = RouteItem.objects.filter(route=route).order_by('date')
    return render(request, 'main/route_item_list.html', {'route': route, 'items': items})
@login_required
def route_list(request):
    trips = Trip.objects.prefetch_related('routes')
    return render(request, 'main/route_list.html', {'trips': trips})

@login_required
def select_trip(request):
    trips = Trip.objects.filter(created_by=request.user)

    if not trips.exists():
        messages.warning(request, "Сначала создайте путешествие.")
        return redirect('trips')  # Редирект на страницу создания путешествия

    return render(request, 'main/select_trip.html', {'trips': trips})


def add_route_item(request, route_id):
    route = get_object_or_404(Route, id=route_id)
    if request.method == "POST":
        form = RouteItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.route = route  # Устанавливаем маршрут
            item.save()
            return redirect('route_item_list', route_id=route.id)
    else:
        form = RouteItemForm()
    return render(request, 'main/add_route_item.html', {'form': form, 'route': route})


@login_required
def route(request):
    trips = Trip.objects.filter(members__user=request.user)  # Получаем все путешествия для текущего пользователя

    # Если у пользователя нет путешествий, выводим сообщение
    if not trips.exists():
        messages.warning(request, "У вас нет путешествий. Пожалуйста, создайте путешествие.")
        return redirect('select_trip')  # Перенаправление на страницу выбора путешествия

    # Отображаем маршруты для всех путешествий пользователя
    return render(request, 'main/route_list.html', {'trips': trips})

@login_required
def delete_route(request, route_id):
    route = get_object_or_404(Route, id=route_id)

    # Проверка: только администратор путешествия может удалять маршруты
    if route.trip.created_by != request.user:
        return HttpResponseForbidden("Вы не можете удалить этот маршрут.")

    if request.method == 'POST':
        route.delete()
        return redirect('route_list')

def edit_route_item(request, item_id):
    item = get_object_or_404(RouteItem, id=item_id)
    if request.method == 'POST':
        form = RouteItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('route_item_list', route_id=item.route.id)
    else:
        form = RouteItemForm(instance=item)
    return render(request, 'main/edit_route_item.html', {'form': form, 'item': item})

def delete_route_item(request, item_id):
    item = get_object_or_404(RouteItem, id=item_id)
    route_id = item.route.id  # Сохраняем ID маршрута, чтобы вернуться на правильную страницу
    if request.method == 'POST':
        item.delete()
        return redirect('route_item_list', route_id=route_id)
    return render(request, 'main/delete_route_item.html', {'item': item})

def budget_view(request):
    routes = Route.objects.all()  # Получаем все маршруты
    return render(request, 'main/budget.html', {'routes': routes})

@login_required
def task_list(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    tasks = trip.tasks.all()  # Получить задачи, связанные с этим путешествием
    return render(request, 'main/tasks.html', {'tasks': tasks, 'trip': trip})

@login_required
def create_task(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    if request.user != trip.creator:
        return redirect('task_list', trip_id=trip.id)

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.trip = trip
            task.save()
            return redirect('task_list', trip_id=trip.id)
    else:
        form = TaskForm()

    return render(request, 'main/create_task.html', {'form': form, 'trip': trip})