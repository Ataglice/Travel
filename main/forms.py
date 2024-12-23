from django import forms
from .models import Route, RouteItem, Task


class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['name']  # Поля, которые будут доступны для заполнения пользователем
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название маршрута'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Описание маршрута'}),
        }


class RouteItemForm(forms.ModelForm):
    class Meta:
        model = RouteItem
        fields = ['route', 'title', 'description', 'date', 'price']
        widgets = {
            'route': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название пункта'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Описание', 'rows': 4}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Цена'}),

        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'trip', 'assigned_to']