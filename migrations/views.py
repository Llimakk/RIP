# from django.http import HttpResponse
# from django.shortcuts import render
# from django.shortcuts import redirect

# from datetime import date

# bills = [
#     {
#         "id":1,
#         "name":"5 рублёвая купюра",
#         "description":"Банкнота изготовлена на высококачественной хлопковой бумаге светло-зеленого оттенка. В бумагу внедрены фиолетовые, красные и светло-зеленые волокна, а также защитная нить, расположенная вертикально и видимая на просвет. Бумага имеет локальные водяные знаки, размещенные слева и справа на купонных полях. Основное изображение лицевой стороны — памятник «Тысячелетие России» на фоне Софийского собора в Великом Новгороде. Основное изображение оборотной стороны — стена Новгородского кремля.",
#         "year":"1 января 1988 года",
#         "imagen": "http://127.0.0.1:9000/lr2/5-rub.png",
#         "imagen_back":"http://127.0.0.1:9000/lr2/5rub-obr.png"
#     },
#     {
#         "id":2,
#         "name":"10 рублёвая купюра",
#         "description":"Модифицированная банкнота имеет формат, цветовое и сюжетное оформление, аналогичное банкноте Банка России образца 1997 года. На лицевой стороне модифицированной банкноты, справа от рельефных знаков для людей с ослабленным зрением находится текст «МОДИФИКАЦИЯ 2004 Г.», который расположен вертикально. Банкнота имеет два серийных номера, расположенных на лицевой стороне банкноты и состоящих из двухбуквенного обозначения серии и семи цифр.",
#         "year":"16 августа 2004 года",
#         "imagen": "http://127.0.0.1:9000/lr2/10-rub.png",
#         "imagen_back":"http://127.0.0.1:9000/lr2/10rub-obr.png"
#     },
#     {
#         "id":3,
#         "name":"50 рублёвая купюра",
#         "description":"Модифицированная банкнота имеет формат, цветовое и сюжетное оформление, аналогичное банкноте Банка России образца 1997 года. На лицевой стороне модифицированной банкноты, справа от рельефных знаков для людей с ослабленным зрением находится текст «МОДИФИКАЦИЯ 2004 Г.», который расположен вертикально. Банкнота имеет два серийных номера, расположенных на лицевой стороне банкноты и состоящих из двухбуквенного обозначения серии и семи цифр.",
#         "year":"16 августа 2004 года",
#         "imagen": "http://127.0.0.1:9000/lr2/50-rub.png",
#         "imagen_back":"http://127.0.0.1:9000/lr2/50rub-obr.png"
#     },
#     {
#         "id":4,
#         "name":"100 рублёвая купюра",
#         "description":"Преобладающие цвета банкноты — оливковый, оранжевый. Основное изображение лицевой стороны банкноты — фрагмент Спасской башни Московского Кремля с курантами. Основное изображение оборотной стороны банкноты — Ржевский мемориал Советскому Cолдату. На лицевой стороне банкноты слева вверху расположен герб Российской Федерации. На оборотной стороне в верхней правой части банкноты находится надпись «2022» — год выпуска банкноты. В нижней правой части лицевой стороны банкноты расположен QR-код, содержащий ссылку на страницу сайта Банка России с описанием защитных признаков банкноты. Банкнота изготовлена на хлопковой бумаге белого цвета.",
#         "year":"30 июня 2022 года",
#         "imagen": "http://127.0.0.1:9000/lr2/100-rub.png",
#         "imagen_back":"http://127.0.0.1:9000/lr2/100rub-obr.png"
#     },
#     {
#         "id":5,
#         "name":"200 рублёвая купюра",
#         "description":"Преобладающий цвет банкноты — зеленый. Основное изображение лицевой стороны банкноты — Памятник затопленным кораблям в г. Севастополе. Основное изображение оборотной стороны банкноты — Государственный историко-архитектурный музей-заповедник «Херсонес Таврический». На оборотной стороне в верхней правой части банкноты находится надпись «2017» — год образца банкноты.В нижней правой части лицевой стороны банкноты расположен QR-код, содержащий ссылку на страницу сайта Банка России с описанием защитных признаков банкноты. Банкнота изготовлена на хлопковой бумаге белого цвета повышенной плотности с полимерной пропиткой. В бумагу внедрены защитные волокна двух типов — цветные с чередующимися участками красного и синего цветов и волокна серого цвета.",
#         "year":"12 октября 2017 года",
#         "imagen": "http://127.0.0.1:9000/lr2/200-rub.png",
#         "imagen_back":"http://127.0.0.1:9000/lr2/200rub-obr.png"
#     },
#     {
#         "id":6,
#         "name":"500 рублёвая купюра",
#         "description":"Модифицированная банкнота имеет формат и сюжетное оформление, аналогичные банкноте Банка России соответствующего номинала модификации 2004 года. Цветовое и художественное оформление лицевой и оборотной сторон частично изменено. На лицевой стороне модифицированной банкноты, в нижней части левого купонного поля слева от основного изображения, находится текст «МОДИФИКАЦИЯ 2010 ГОДА». Банкнота имеет два серийных номера, расположенных на лицевой стороне банкноты и состоящих из двухбуквенного обозначения серии и семи цифр.",
#         "year":"6 сентября 2011 года",
#         "imagen": "http://127.0.0.1:9000/lr2/500-rub.png",
#         "imagen_back":"http://127.0.0.1:9000/lr2/500rub-obr.png"
#     },
#     {
#         "id":7,
#         "name":"1000 рублёвая купюра",
#         "description":"Модифицированная банкнота имеет формат и сюжетное оформление, аналогичные банкноте Банка России соответствующего номинала модификации 2004 года. Цветовое оформление банкноты претерпело незначительное изменение. На лицевой стороне модифицированной банкноты, в нижней части широкого купонного поля справа от основного изображения, находится текст «МОДИФИКАЦИЯ 2010 ГОДА». Банкнота имеет два серийных номера, расположенных на лицевой стороне банкноты и состоящих из двухбуквенного обозначения серии и семи цифр.",
#         "year":"10 августа 2010 года",
#         "imagen": "http://127.0.0.1:9000/lr2/1000-rub.png",
#         "imagen_back":"http://127.0.0.1:9000/lr2/1000rub-obr.png"
#     },
#     {
#         "id":8,
#         "name":"2000 рублёвая купюра",
#         "description":"Преобладающий цвет банкноты — синий. Основное изображение лицевой стороны банкноты — Русский мост — вантовый мост в г. Владивостоке, соединяющий остров Русский с материковой частью г. Владивостока. Основное изображение оборотной стороны банкноты — космодром «Восточный». Банкнота изготовлена на хлопковой бумаге белого цвета. В бумагу внедрены защитные волокна двух типов — цветные с чередующимися участками красного и синего цветов и волокна серого цвета. Ныряющая голографическая защитная нить шириной 5 мм выходит на поверхность лицевой стороны банкноты в окнах фигурной формы.",
#         "year":"12 октября 2017 года",
#         "imagen": "http://127.0.0.1:9000/lr2/2000-rub.png",
#         "imagen_back":"http://127.0.0.1:9000/lr2/2000rub-obr.png"
#     },
#     {
#         "id":9,
#         "name":"5000 рублёвая купюра",
#         "description":"Преобладающий цвет банкноты — красный. Основное изображение лицевой стороны банкноты — стела «Европа — Азия». Основное изображение оборотной стороны банкноты — памятник «Сказ об Урале» в Челябинске. Банкнота изготовлена на хлопковой бумаге белого цвета. В бумагу внедрены защитные волокна двух типов — цветные с чередующимися участками красного и синего цветов и волокна серого цвета. Голографическая защитная нить шириной 5,5 мм выходит на поверхность лицевой стороны банкноты в окне фигурной формы.",
#         "year":"16 октября 2023 года",
#         "imagen": "http://127.0.0.1:9000/lr2/5000-rub.png",
#         "imagen_back":"http://127.0.0.1:9000/lr2/5000rub-obr.png"
#     }
# ]

# pick_operat = {
#     "id": 147,
#     "current_date": date.today(),
#     "bills": [
#         {
#             "id": 1,
#             "name": "5 рублёвая купюра",
#             "operation": "снятие наличных",
#             "imagen": "http://127.0.0.1:9000/lr2/5-rub.png",
#             "count": 10
#         },
#         {
#             "id": 4,
#             "name": "100 рублёвая купюра",
#             "operation": "снятие наличных",
#             "imagen": "http://127.0.0.1:9000/lr2/100-rub.png",
#             "count": 20
#         },
#         {
#             "id": 7,
#             "name": "1000 рублёвая купюра",
#             "operation": "снятие наличных",
#             "imagen": "http://127.0.0.1:9000/lr2/1000-rub.png",
#             "count": 3
#         }
#     ]
# }

# def getBillById(bill_id):
#     for bill in bills:
#         if bill["id"] == bill_id:
#             return bill
        
# def bill(request, bill_id):
#     context = {
#         "id": bill_id,
#         "bill": getBillById(bill_id),
#     }

#     return render(request, "bill.html", context)

# def getPickOperat():
#     return pick_operat

# def getOperatById(operat_id):
#     return pick_operat

# def searchBills(bill_name):
#     res = []

#     for bill in bills:
#         if bill_name.lower() in bill["name"].lower():
#             res.append(bill)

#     return res

# def Index(request):
#     search_bill = request.GET.get("banknotes", "")
#     bills = searchBills(search_bill)
#     pick_operat = getPickOperat()
#     cart_count = len(cart)

#     context = {
#         "bills": bills,
#         "banknotes": search_bill,
#         "bills_count": len(pick_operat["bills"]),
#         "pick_operat": pick_operat,
#         "cart_count": cart_count
#     }

#     return render(request, "bills.html", context)

# cart = []

# def operat(request, operat_id):
#     context = {
#         "operat": getOperatById(operat_id),
#         "cart": cart,  # Добавляем корзину в контекст
#     }
#     return render(request, "operat.html", context)


# def add_to_cart(request, bill_id):
#     if request.method == "POST":
#         bill = getBillById(bill_id)
#         if bill:
#             cart.append(bill)  # Добавляем товар в корзину
#     return redirect('index')  # Перенаправляем на главную страницу (или корзину)

# def clear_cart(request):
#     if request.method == "POST":
#         global cart  # Используем глобальную корзину
#         cart.clear()  # Очищаем список товаров в корзине
#         return render(request, 'operat.html', {
#             'operat': getOperatById(147),  # Передаем операцию
#             'cart': cart,  # Пустая корзина
#             'message': 'Заявка удалена'  # Сообщение об удалении
#         })