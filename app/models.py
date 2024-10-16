from django.db import models
from datetime import date
from django.utils import timezone

from django.contrib.auth.models import User

from app.utils import STATUS_CHOICES


class Bill(models.Model):
    STATUS_CHOICES = (
        (1, 'Действует'),
        (2, 'Удален'),
    )

    name = models.CharField(max_length=100, verbose_name="Название")
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="Статус")
    image = models.CharField(default="images/default.png")
    image_back = models.CharField(default="images/default.png")
    year = models.CharField(max_length=100, default="1988")
    description = models.TextField(verbose_name="Описание", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Купюра"
        verbose_name_plural = "Купюры"
        db_table = "bills"


class Operat(models.Model):
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="Статус")
    date_created = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")
    date_formation = models.DateTimeField(verbose_name="Дата формирования", blank=True, null=True)
    date_complete = models.DateTimeField(verbose_name="Дата завершения", blank=True, null=True)
    address = models.CharField(max_length=255, default="г. Москва, ул. Мирная 11, д. 2")
    value = models.IntegerField(default=0)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь", null=True, related_name='owner')
    moderator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Модератор", null=True, related_name='moderator')

    def __str__(self):
        return f"Операция №{self.id}"

    def get_bills(self):
        res = []

        for item in BillOperat.objects.filter(operat=self):
            product = item.bill
            product.value = item.value
            res.append(product)

        return res

    def get_status(self):
        return dict(STATUS_CHOICES).get(self.status)

    class Meta:
        verbose_name = "Снятие наличных"
        ordering = ('-date_formation', )
        db_table = "operation"


class BillOperat(models.Model):
    id_bill_mm = models.ForeignKey(Bill, on_delete=models.CASCADE)
    id_operat_mm = models.ForeignKey(Operat, on_delete=models.CASCADE)
    value = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.count}x {self.id_bill_mm.name} в операции {self.id_operat_mm.id}"

    class Meta:
        unique_together = (('id_bill_mm', 'id_operat_mm'),) 
        verbose_name = "Купюра-Снятие"
        verbose_name_plural = "Купюры-Снятие"
        db_table = "bill_operat"