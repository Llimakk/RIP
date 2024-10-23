from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db import connection
from app.models import Bill, Operat, BillOperat
from django.contrib.auth.models import User
from django.http import HttpResponse


def get_current_user(request):
    return request.user  # Возвращает текущего аутентифицированного пользователя


def index(request):
    search_bill = request.GET.get("banknotes", "")

    # Поиск купюр в базе данных
    bills = Bill.objects.filter(name__icontains=search_bill, status=1)

    # Получение текущей незавершенной операции
    pick_operat = get_pick_operat(request)

    # Получаем количество товаров в корзине из сессии
    cart = request.session.get('cart', [])

    context = {
        "bills": bills,
        "banknotes": search_bill,
        "bills_count": len(pick_operat.get_bills()) if pick_operat else 0,
        "pick_operat": pick_operat,
        "cart_count": len(cart)
    }

    return render(request, "bills.html", context)

def get_pick_operat(request):
    """Получаем текущую операцию (draft) для пользователя"""
    user = get_current_user(request)
    if not user.is_authenticated:
        return None
    
    operat = Operat.objects.filter(status=1, owner=user).first()
    
    # Если операции нет, создаем новую
    if not operat:
        operat = Operat.objects.create(owner=user, status=1, date_created=timezone.now())
    
    return operat


def bill(request, bill_id):
    # Получаем купюру по ID
    bill = get_object_or_404(Bill, pk=bill_id)

    context = {
        "bill": bill,
    }

    return render(request, "bill.html", context)


def operat(request, operat_id):
    # Получаем операцию по ID
    operat = get_object_or_404(Operat, pk=operat_id)
    
    # Получаем корзину из сессии
    cart = request.session.get('cart', [])

    bills_in_cart = Bill.objects.filter(id__in=cart)

    context = {
        "operat": operat,
        "cart": bills_in_cart,  # Добавляем корзину в контекст
    }
    return render(request, "operat.html", context)


def add_to_cart(request, bill_id):
    if request.method == "POST":
        bill = get_object_or_404(Bill, pk=bill_id)  # Получаем купюру из БД
        if bill:
            # Получаем корзину из сессии или создаем новую
            cart = request.session.get('cart', [])
            cart.append(bill.id)  # Добавляем ID купюры в корзину
            request.session['cart'] = cart  # Сохраняем корзину в сессию
    return redirect('index')  # Перенаправляем на главную страницу (или корзину)

def clear_cart(request):
    if request.method == "POST":
        # Получаем текущую операцию
        operat = get_pick_operat(request)

        if operat:
            # Очищаем корзину в сессии
            request.session['cart'] = []

            # Выполняем SQL-запрос для обновления статуса операции на "Удален" (5)
            with connection.cursor() as cursor:
                cursor.execute("UPDATE operation SET status = %s WHERE id = %s", [5, operat.id])

            return redirect('index')  # Перенаправляем на главную страницу

    return render(request, 'operat.html', {
        'operat': operat,  # Передаем текущую операцию
        'cart': [],  # Пустая корзина
        'message': 'Корзина очищена и операция удалена'  # Сообщение об удалении
    })


def add_bill_to_operat(request, bill_id):
    bill = get_object_or_404(Bill, pk=bill_id)
    operat = get_pick_operat(request)

    if not operat:
        # Если нет черновика операции, создаем новый
        operat = Operat.objects.create(owner=get_current_user(request), status=1, date_created=timezone.now())

    # Проверяем, есть ли уже эта купюра в операции
    if BillOperat.objects.filter(id_bill_mm=bill, id_operat_mm=operat).exists():
        return redirect('index')

    # Создаем запись в BillOperat
    BillOperat.objects.create(id_bill_mm=bill, id_operat_mm=operat, value=1)

    return redirect('operat', operat_id=operat.id)


def complete_operat(request, operat_id):
    operat = get_object_or_404(Operat, pk=operat_id)

    operat.status = 1 
    operat.date_complete = timezone.now()
    operat.save()

    return redirect('index')
