from rest_framework.decorators import api_view
from rest_framework.response import Response
from main.models import Trip, TripMember, Task, Expense, Message
from .serializers import TripSerializer, TripMemberSerializer, TaskSerializer, ExpenseSerializer, MessageSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import UserRegistrationSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trip_list(request):
    trips = Trip.objects.all()  # Получаем все путешествия
    serializer = TripSerializer(trips, many=True)  # Сериализуем путешествия
    return Response(serializer.data)  # Отправляем данные в JSON формате

@api_view(['GET'])
def trip_detail(request, trip_id):
    try:
        trip = Trip.objects.get(id=trip_id)
    except Trip.DoesNotExist:
        return Response({"error": "Trip not found"}, status=404)
    serializer = TripSerializer(trip)  # Сериализуем одно путешествие
    return Response(serializer.data)

@api_view(['GET'])
def trip_member_list(request):
    members = TripMember.objects.all()  # Получаем всех участников
    serializer = TripMemberSerializer(members, many=True)  # Сериализуем участников
    return Response(serializer.data)

@api_view(['GET'])
def task_list(request):
    tasks = Task.objects.all()  # Получаем все задачи
    serializer = TaskSerializer(tasks, many=True)  # Сериализуем задачи
    return Response(serializer.data)

@api_view(['GET'])
def expense_list(request):
    expenses = Expense.objects.all()  # Получаем все расходы
    serializer = ExpenseSerializer(expenses, many=True)  # Сериализуем расходы
    return Response(serializer.data)

@api_view(['GET'])
def message_list(request):
    messages = Message.objects.all()  # Получаем все сообщения
    serializer = MessageSerializer(messages, many=True)  # Сериализуем сообщения
    return Response(serializer.data)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return Response({"access": access_token}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Создаем пользователя
            return Response({'message': 'User created successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            # Генерация токенов
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)