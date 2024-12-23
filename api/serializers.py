from rest_framework import serializers
from main.models import Trip, TripMember, Task, Expense, Message
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class TripSerializer(serializers.ModelSerializer):
    created_by = UserSerializer()  # Встраиваем информацию о пользователе (создателе)

    class Meta:
        model = Trip
        fields = ['id', 'name', 'destination', 'start_date', 'end_date', 'created_by', 'created_at']


class TripMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Встраиваем информацию о пользователе (участнике)
    trip = TripSerializer()  # Встраиваем информацию о путешествии

    class Meta:
        model = TripMember
        fields = ['id', 'user', 'role', 'joined_at', 'trip']


class TaskSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer()  # Встраиваем информацию о пользователе (назначенном на задачу)
    trip = TripSerializer()  # Встраиваем информацию о путешествии

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'assigned_to', 'is_completed', 'created_at', 'trip']


class ExpenseSerializer(serializers.ModelSerializer):
    paid_by = UserSerializer()  # Встраиваем информацию о пользователе (оплатившем расход)
    trip = TripSerializer()  # Встраиваем информацию о путешествии

    class Meta:
        model = Expense
        fields = ['id', 'name', 'amount', 'paid_by', 'created_at', 'trip']


class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Встраиваем информацию о пользователе (отправившем сообщение)
    trip = TripSerializer()  # Встраиваем информацию о путешествии

    class Meta:
        model = Message
        fields = ['id', 'user', 'message', 'created_at', 'trip']


from rest_framework import serializers
from django.contrib.auth.models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Пароль только для записи

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user