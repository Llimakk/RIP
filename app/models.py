from django.db import models
from datetime import date
from django.utils import timezone
from django.contrib.auth.models import User

class Bill(models.Model):
    STATUS_CHOICES = (
        (1, 'Действует'),
        (2, 'Удален'),
    )

    name = models.CharField(max_length=100, verbose_name="Название")
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="Статус")
    image = models.CharField(max_length=100, default="images/default.png")
    year = models.CharField(max_length=100, default="1988")
    description = models.TextField(verbose_name="Описание", blank=True)
    

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Купюра"
        verbose_name_plural = "Купюры"
        db_table = "bills"


class Operat(models.Model):
    STATUS_CHOICES = [
        (1, 'Введён'),
        (2, 'В работе'),
        (3, 'Завершен'),
        (4, 'Отклонен'),
        (5, 'Удален')
    ]

    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="Статус")
    date_created = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")
    date_formation = models.DateTimeField(verbose_name="Дата формирования", blank=True, null=True)
    date_complete = models.DateTimeField(verbose_name="Дата завершения", blank=True, null=True)
    address = models.CharField(max_length=255, default="г. Москва, ул. Мирная 11, д. 2")
    # count = models.IntegerField(default=1)
    success = models.BooleanField(blank=True, null=True)

    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="Создатель", related_name='owner', null=True)
    moderator = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="Модератор", related_name='moderator', blank=True,  null=True)
    manager = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="Менежер", related_name='manager', blank=True,  null=True)

    def __str__(self):
        return f"Операция №{self.id}"

    class Meta:
        verbose_name = "Операция снятия наличных"
        verbose_name_plural = "Операции снятия нальчных"
        db_table = "operats"


class BillOperat(models.Model):
    bill = models.ForeignKey(Bill, models.CASCADE, blank=True, null=True)
    operat = models.ForeignKey(Operat, models.CASCADE, blank=True, null=True)
    count = models.IntegerField(verbose_name="Колличество", default=1)

    def __str__(self):
        return "м-м №" + str(self.pk)

    class Meta:
        unique_together = (('bill', 'operat'),) 
        verbose_name = "Купюра-Операция"
        verbose_name_plural = "Купюры-Операции"
        db_table = 'bill_operat'