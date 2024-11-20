from django.http import HttpResponse
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt


def get_draft_operat():
    return Operat.objects.filter(status=1).first()

def get_user():
    user = User.objects.filter(is_superuser=False).first()
    if user is None:
        raise ValueError("Default user not found.")
    return user


def get_moderator():
    return User.objects.filter(is_superuser=True).first()


@api_view(["GET"])
def search_bills(request):
    query = request.GET.get("query", "")

    bills = Bill.objects.filter(status=1).filter(name__icontains=query)

    serializer = BillSerializer(bills, many=True)

    draft_operat = get_draft_operat()

    resp = {
        "bills": serializer.data,
        "draft_operat": draft_operat.pk if draft_operat else None,
        "bills_count": bills.count()
    }

    return Response(resp)


@api_view(["GET"])
def get_bill_by_id(request, bill_id):
    if not Bill.objects.filter(pk=bill_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    bill = Bill.objects.get(pk=bill_id)
    serializer = BillSerializer(bill, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
def update_bill(request, bill_id):
    if not Bill.objects.filter(pk=bill_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    bill = Bill.objects.get(pk=bill_id)

    image = request.data.get("image")
    if image is not None:
        bill.image = image
        bill.save()

    serializer = BillSerializer(bill, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["POST"])
def create_bill(request):
    Bill.objects.create()

    bills = Bill.objects.filter(status=1)
    serializer = BillSerializer(bills, many=True)

    return Response(serializer.data)


@api_view(["DELETE"])
def delete_bill(request, bill_id):
    if not Bill.objects.filter(pk=bill_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    bill = Bill.objects.get(pk=bill_id)
    bill.status = 2
    bill.save()

    bills = Bill.objects.filter(status=1)
    serializer = BillSerializer(bills, many=True)

    return Response(serializer.data)


@csrf_exempt
@api_view(['POST'])
def add_bill_to_operat(request, bill_id):
    if not Bill.objects.filter(pk=bill_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    bill = Bill.objects.get(pk=bill_id)

    draft_operat = get_draft_operat()

    if draft_operat is None:
        draft_operat = Operat.objects.create()
        draft_operat.owner = get_user()  # Используем get_user() без self
        draft_operat.date_created = timezone.now()
        draft_operat.save()

    if BillOperat.objects.filter(operat=draft_operat, bill=bill).exists():
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    item = BillOperat.objects.create()
    item.operat = draft_operat
    item.bill = bill
    item.save()

    serializer = OperatSerializer(draft_operat, many=False)

    return Response(serializer.data["bills"])


@api_view(["PUT"])
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
def search_operats(request):
    status = int(request.GET.get("status", 0))
    date_formation_start = request.GET.get("date_formation_start")
    date_formation_end = request.GET.get("date_formation_end")

    operats = Operat.objects.exclude(status__in=[1, 5])

    if status > 0:
        operats = operats.filter(status=status)

    if date_formation_start and parse_datetime(date_formation_start):
        operats = operats.filter(date_formation__gte=parse_datetime(date_formation_start))

    if date_formation_end and parse_datetime(date_formation_end):
        operats = operats.filter(date_formation__lt=parse_datetime(date_formation_end))

    serializer = OperatsSerializer(operats, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def get_operat_by_id(request, operat_id):
    if not Operat.objects.filter(pk=operat_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    operat = Operat.objects.get(pk=operat_id)
    serializer = OperatSerializer(operat, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
def update_operat(request, operat_id):
    if not Operat.objects.filter(pk=operat_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    operat = Operat.objects.get(pk=operat_id)
    serializer = OperatSerializer(operat, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["PUT"])
def update_status_user(request, operat_id):
    if not Operat.objects.filter(pk=operat_id).exists():
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
def update_status_admin(request, operat_id):
    if not Operat.objects.filter(pk=operat_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    request_status = int(request.data["status"])

    if request_status not in [3, 4]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    operat = Operat.objects.get(pk=operat_id)

    if operat.status != 2:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    operat.date_complete = timezone.now()
    operat.status = request_status
    operat.moderator = get_moderator()
    operat.save()

    serializer = OperatSerializer(operat, many=False)

    return Response(serializer.data)


@api_view(["DELETE"])
def delete_operat(request, operat_id):
    if not Operat.objects.filter(pk=operat_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    operat = Operat.objects.get(pk=operat_id)

    if operat.status != 1:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    operat.status = 5
    operat.save()

    serializer = OperatSerializer(operat, many=False)

    return Response(serializer.data)


@api_view(["DELETE"])
def delete_bill_from_operat(request, operat_id, bill_id):
    if not BillOperat.objects.filter(operat_id=operat_id, bill_id=bill_id).exists():
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


@api_view(["PUT"])
def update_bill_in_operat(request, operat_id, bill_id):
    if not BillOperat.objects.filter(bill_id=bill_id, operat_id=operat_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    item = BillOperat.objects.get(bill_id=bill_id, operat_id=operat_id)

    serializer = BillOperatSerializer(item, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["POST"])
def register(request):
    serializer = UserRegisterSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(status=status.HTTP_409_CONFLICT)

    user = serializer.save()

    serializer = UserSerializer(user)

    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["PUT"])
def update_user(request, user_id):
    if not User.objects.filter(pk=user_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = User.objects.get(pk=user_id)
    serializer = UserSerializer(user, data=request.data, many=False, partial=True)

    if not serializer.is_valid():
        return Response(status=status.HTTP_409_CONFLICT)

    serializer.save()

    return Response(serializer.data)