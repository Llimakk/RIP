from django.http import HttpResponse
import requests
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from datetime import date
import uuid
import random
import redis
import psycopg2
from django.db import connection
from .models import *
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from django.utils.dateparse import parse_datetime
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .permissions import *
import logging
from .serializers import *
from django.core.cache import cache
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import logout as django_logout
from random import randint

logger = logging.getLogger(__name__)
session_storage = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

def get_draft_operat(request):
    session_id = request.COOKIES.get("session_id")
    if not session_id:
        return None  # возвращаем None, если session_id отсутствует

    username = session_storage.get(session_id)
    if not username:
        return None  # возвращаем None, если пользователь не найден в сессии

    username = username.decode('utf-8')
    try:
        current_user = User.objects.get(username=username)
    except User.DoesNotExist:
        return None  # возвращаем None, если пользователь не найден в базе данных

    return Operat.objects.filter(owner=current_user, status=1).first()  # возвращаем первый черновик или None


@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter(
            'query',
            openapi.IN_QUERY,
            type=openapi.TYPE_STRING
        )
    ]
)


@api_view(["GET"])
def search_bills(request):
    bill_name = request.GET.get("bill_name", "")

    bills = Bill.objects.filter(status=1)

    if bill_name:
        bills = bills.filter(name__icontains=bill_name)

    serializer = BillSerializer(bills, many=True)

    draft_operat = get_draft_operat(request)

    resp = {
        "bills": serializer.data,
        "bills_count": BillOperat.objects.filter(operat=draft_operat).count() if draft_operat else None,
        "draft_operat_id": draft_operat.pk if draft_operat else None
    }

    return Response(resp)


@api_view(["GET"])
def get_bill_by_id(request, bill_id):
    if not Bill.objects.filter(pk=bill_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    bill = Bill.objects.get(pk=bill_id)
    serializer = BillSerializer(bill, many=False)

    return Response(serializer.data)


@swagger_auto_schema(method='put', request_body=BillSerializer)
@api_view(["PUT"])
@permission_classes([IsModerator])
def update_bill(request, bill_id):
    if not Bill.objects.filter(pk=bill_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    bill = Bill.objects.get(pk=bill_id)

    name = request.data.get("name")
    if name is not None:
        bill.image = name
        bill.save()

    serializer = BillSerializer(bill, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsModerator])
def create_bill(request):
    Bill.objects.create()

    bills = Bill.objects.filter(status=1)
    serializer = BillSerializer(bills, many=True)

    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsModerator])
def delete_bill(request, bill_id):
    if not Bill.objects.filter(pk=bill_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    bill = Bill.objects.get(pk=bill_id)
    bill.status = 2
    bill.save()

    bills = Bill.objects.filter(status=1)
    serializer = BillSerializer(bills, many=True)

    return Response(serializer.data)


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
def add_bill_to_operat(request, bill_id):
    try:
        username = session_storage.get(request.COOKIES["session_id"])
        username = username.decode('utf-8')
    except:
        return Response(
            {"Message": "Нет авторизованных пользователей"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    user = get_object_or_404(User, username=username)


    if not Bill.objects.filter(pk=bill_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    bill = Bill.objects.get(pk=bill_id)

    draft_operat = Operat.objects.filter(owner=user).filter(status=1).first()

    if draft_operat is None:
        draft_operat = Operat.objects.create(
            owner=user
        )
        draft_operat.save()

    if BillOperat.objects.filter(operat=draft_operat, bill=bill).exists():
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    item = BillOperat.objects.create()
    item.operat = draft_operat
    item.bill = bill
    item.save()

    serializer = OperatSerializer(draft_operat)

    return Response(serializer.data["bills"])

@swagger_auto_schema(method='put', request_body=BillSerializer)
@api_view(["PUT"])
@permission_classes([IsModerator])
def update_bill_image(request, bill_id):
    if not Bill.objects.filter(pk=bill_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    bill = Bill.objects.get(pk=bill_id)

    image = request.data.get("image")
    if image is not None:
        bill.image = image
        bill.save()

    serializer = BillSerializer(bill)

    return Response(serializer.data)


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def search_operats(request):
    status = int(request.GET.get("status", 0))
    date_formation_start = request.GET.get("date_formation_start")
    date_formation_end = request.GET.get("date_formation_end")

    operats = Operat.objects.exclude(status__in=[1, 5])

    try:
        username = session_storage.get(request.COOKIES["session_id"])
        username = username.decode('utf-8')
    except:
        return Response(
            {"Message": "Нет авторизованных пользователей"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    user = get_object_or_404(User, username=username)
    
    if not user.is_staff:
        operats = operats.filter(owner=user)

    if status > 0:
        operats = operats.filter(status=status)

    if date_formation_start and parse_datetime(date_formation_start):
        operats = operats.filter(date_formation__gte=parse_datetime(date_formation_start))

    if date_formation_end and parse_datetime(date_formation_end):
        operats = operats.filter(date_formation__lt=parse_datetime(date_formation_end))

    serializer = OperatSerializer(operats, many=True)

    return Response(serializer.data)


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def get_operat_by_id(request, operat_id):
    username = session_storage.get(request.COOKIES["session_id"])
    username = username.decode('utf-8')
    user = get_object_or_404(User, username=username)

    if not Operat.objects.filter(pk=operat_id, owner=user).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    operat = Operat.objects.get(pk=operat_id)
    serializer = OperatSerializer(operat, many=False)

    return Response(serializer.data)

@swagger_auto_schema(method='put', request_body=OperatSerializer)
# @permission_classes([IsAuthenticated])
@api_view(["PUT"])
def update_operat(request, operat_id):
    try:
        username = session_storage.get(request.COOKIES["session_id"])
        username = username.decode('utf-8')
    except:
        return Response(
            {"Message": "Нет авторизованных пользователей"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    user = get_object_or_404(User, username=username)

    if not Operat.objects.filter(pk=operat_id, owner=user).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    operat = Operat.objects.get(pk=operat_id)
    serializer = OperatSerializer(operat, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["PUT"])
# @permission_classes([IsAuthenticated])
def update_status_user(request, operat_id):
    try:
        username = session_storage.get(request.COOKIES["session_id"])
        username = username.decode('utf-8')
    except:
        return Response(
            {"Message": "Нет авторизованных пользователей"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    user = get_object_or_404(User, username=username)

    if not Operat.objects.filter(pk=operat_id, owner=user).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    operat = Operat.objects.get(pk=operat_id)

    if operat.status != 1:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    operat.status = 2
    operat.date_formation = timezone.now()
    operat.save()

    serializer = OperatSerializer(operat, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsModerator])
def update_status_admin(request, operat_id):
    if not Operat.objects.filter(pk=operat_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    request_status = int(request.data["status"])

    if request_status not in [3, 4]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    operat = Operat.objects.get(pk=operat_id)

    if operat.status != 2:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    if request_status == 3:
        operat.success = True if randint(1, 2) == 1 else False
    
    username = session_storage.get(request.COOKIES["session_id"])
    username = username.decode('utf-8')

    user = User.objects.get(username=username)
    operat.date_complete = timezone.now()
    operat.status = request_status
    operat.moderator = user
    operat.save()

    serializer = OperatSerializer(operat, many=False)

    return Response(serializer.data)


@api_view(["DELETE"])
# @permission_classes([IsAuthenticated])
def delete_operat(request, operat_id):
    try:
        username = session_storage.get(request.COOKIES["session_id"])
        username = username.decode('utf-8')
    except:
        return Response(
            {"Message": "Нет авторизованных пользователей"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    user = get_object_or_404(User, username=username)

    if not Operat.objects.filter(pk=operat_id, owner=user).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    operat = Operat.objects.get(pk=operat_id)

    if operat.status != 1:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    operat.status = 5
    operat.save()

    serializer = OperatSerializer(operat, many=False)

    return Response(serializer.data)


@api_view(["DELETE"])
# @permission_classes([IsAuthenticated])
def delete_bill_from_operat(request, operat_id, bill_id):
    try:
        username = session_storage.get(request.COOKIES["session_id"])
        username = username.decode('utf-8')
    except:
        return Response(
            {"Message": "Нет авторизованных пользователей"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    user = get_object_or_404(User, username=username)

    if not BillOperat.objects.filter(operat_id=operat_id, bill_id=bill_id, owner=user).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    item = BillOperat.objects.get(operat_id=operat_id, bill_id=bill_id)
    item.delete()

    operat = Operat.objects.get(pk=operat_id)

    serializer = OperatSerializer(operat, many=False)
    bills = serializer.data["bills"]

    if len(bills) == 0:
        operat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response(bills)

@swagger_auto_schema(method='PUT', request_body=BillOperatSerializer)
@api_view(["PUT"])
# @permission_classes([IsAuthenticated])
def update_bill_in_operat(request, operat_id, bill_id):
    try:
        username = session_storage.get(request.COOKIES["session_id"])
        username = username.decode('utf-8')
    except:
        return Response(
            {"Message": "Нет авторизованных пользователей"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    user = get_object_or_404(User, username=username)

    if not BillOperat.objects.filter(bill_id=bill_id, operat_id=operat_id, owner=user).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    item = BillOperat.objects.get(bill_id=bill_id, operat_id=operat_id)

    serializer = BillOperatSerializer(item, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@swagger_auto_schema(method='post', request_body=UserLoginSerializer)
@api_view(["POST"])
def login(request):
    try:
        if request.COOKIES["session_id"] is not None:
            return Response({'status': 'Уже в системе'}, status=status.HTTP_403_FORBIDDEN)
    except:
        username = str(request.data["username"]) 
        password = request.data["password"]
        user = authenticate(request, username=username, password=password)
        logger.error(user)
        if user is not None:
            random_key = str(uuid.uuid4()) 
            session_storage.set(random_key, username)

            response = Response({'status': f'{username} успешно вошел в систему'})
            response.set_cookie("session_id", random_key)

            return response
        else:
            return HttpResponse("{'status': 'error', 'error': 'login failed'}")


@swagger_auto_schema(method='post', request_body=UserRegisterSerializer)
@api_view(["POST"])
def register(request):
    try:
        if request.COOKIES["session_id"] is not None:
            return Response({'status': 'Уже в системе'}, status=status.HTTP_403_FORBIDDEN)
    except:
        if User.objects.filter(username = request.data['username']).exists(): 
            return Response({'status': 'Exist'}, status=400)
        serializer = UserRegisterSerializer(data=request.data) 
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        # Получаем session_id из cookies
        session_id = request.COOKIES.get("session_id")
        if not session_id:
            return Response({"Message": "Сессия не найдена"}, status=400)
        
        # Извлекаем имя пользователя из Redis
        username = session_storage.get(session_id)
        if not username:
            return Response({"Message": "Пользователь не найден в сессии"}, status=400)

        username = username.decode('utf-8')
        
        # Вызов стандартного logout для завершения сессии
        django_logout(request)

        # Формируем ответ
        response = Response({'Message': f'{username} вышел из системы'}, status=200)

        # Удаляем cookie с session_id
        response.delete_cookie('session_id')
        
        return response

    except KeyError as e:
        # Ошибка, если нет cookies или проблем с извлечением данных из Redis
        return Response({"Message": "Нет авторизованных пользователей"}, status=403)

    except Exception as e:
        # Логирование ошибки (например, ошибка Redis)
        return Response({"Message": f"Ошибка: {str(e)}"}, status=500)



@swagger_auto_schema(method='PUT', request_body=UserSerializer)
@api_view(["PUT"])
# @permission_classes([IsAuthenticated])
def update_user(request, user_id):
    if not User.objects.filter(pk=user_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    try:
        username = session_storage.get(request.COOKIES["session_id"])
        username = username.decode('utf-8')
    except:
        return Response(
            {"Message": "Нет авторизованных пользователей"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    user = get_object_or_404(User, username=username)

    if user.pk != user_id:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user, data=request.data, partial=True)
    if not serializer.is_valid():
        return Response(status=status.HTTP_409_CONFLICT)

    serializer.save()

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsManager])
def restore_bill(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id, status=2) 

    bill.status = 1  
    bill.save()

    return Response({
        "message": f"Купюра '{bill.name}' восстановлена и теперь доступна.",
        "bill": {
            "id": bill.id,
            "name": bill.name,
            "status": bill.status,
        }
    }, status=status.HTTP_200_OK)