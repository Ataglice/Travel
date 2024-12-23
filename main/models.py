import uuid
from django.db import models
from django.contrib.auth.models import User  # Используем встроенную модель пользователя Django
from django.db.models import Sum
from django.urls import reverse

class Trip(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название путешествия')
    destination = models.CharField(max_length=200, verbose_name='Пункт назначения')
    start_date = models.DateField(verbose_name='Дата начала')
    end_date = models.DateField(verbose_name='Дата окончания')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_trips', verbose_name='Создатель')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    invite_code = models.CharField(max_length=36, unique=True, default=uuid.uuid4, editable=False)


    def __str__(self):
        return self.name

    def invite_url(self):
        return reverse('join_trip', kwargs={'invite_code': self.invite_code})


class TripMember(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Администратор'),
        ('member', 'Участник'),
    ]
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='members', verbose_name='Путешествие')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trips', verbose_name='Пользователь')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member', verbose_name='Роль')
    joined_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата вступления')

    def __str__(self):
        return f"{self.user.username} - {self.role} ({self.trip.name})"


class Task(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='tasks', verbose_name='Путешествие')
    title = models.CharField(max_length=200, verbose_name='Название задания')
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    assigned_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='tasks', verbose_name='Назначен')
    is_completed = models.BooleanField(default=False, verbose_name='Выполнено')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')


    def __str__(self):
        return self.title


class Expense(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='expenses', verbose_name='Путешествие')
    name = models.CharField(max_length=200, verbose_name='Название расхода')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма')
    paid_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='expenses', verbose_name='Оплатил')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')


    def __str__(self):
        return f"{self.name} - {self.amount}"


class Message(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='messages', verbose_name='Путешествие')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages', verbose_name='Пользователь')
    message = models.TextField(verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')

    def __str__(self):
        return f"Message by {self.user.username} in {self.trip.name}"

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class RouteItem(models.Model):
    route = models.ForeignKey('Route', on_delete=models.CASCADE, related_name='items')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)


    def __str__(self):
        return self.title

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    route_item = models.ForeignKey(RouteItem, on_delete=models.CASCADE, related_name="votes")
    is_upvote = models.BooleanField()  # True = за, False = против

class Route(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='routes')
    name = models.CharField(max_length=200)  # Название маршрута
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(verbose_name="Описание маршрута", blank=True)

    def total_budget(self):
        return self.items.aggregate(total=Sum('price'))['total'] or 0

    def __str__(self):
        return f"{self.name} для {self.trip.name}"

class RouteVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="votes")
    is_upvote = models.BooleanField()  # Голос: за или против

    class Meta:
        unique_together = ('user', 'route')  # Один пользователь = один голос

    def __str__(self):
        return f"Vote by {self.user} on {self.route}"