from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User

from app.utils import STATUS_CHOICES


class Bill(models.Model):
    STATUS_CHOICES = (
        (1, 'Действует'),
        (2, 'Удален'),
    )

    name = models.CharField(max_length=100, verbose_name="Название")
    image = models.ImageField(default="images/default.png")
    description = models.TextField(verbose_name="Описание", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Купюра"
        verbose_name_plural = "Купюры"
        db_table = "bills"


class Operat(models.Model):
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="Статус")
    date_created = models.DateTimeField(default=timezone.now(), verbose_name="Дата создания")
    date_formation = models.DateTimeField(verbose_name="Дата формирования", blank=True, null=True)
    date_complete = models.DateTimeField(verbose_name="Дата завершения", blank=True, null=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь", null=True, related_name='owner')
    moderator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Модератор", null=True, related_name='moderator')

    def __str__(self):
        return "Заявка №" + str(self.pk)

    def get_bills(self):
        res = []

        for item in BillOperat.objects.filter(operat=self):
            tmp = item.bill
            tmp.value = item.value
            res.append(tmp)

        return res

    def get_status(self):
        return dict(STATUS_CHOICES).get(self.status)

    class Meta:
        verbose_name = "Снятие наличных"
        ordering = ('-date_formation', )
        db_table = "operat"


class BillOperat(models.Model):
    bill = models.ForeignKey(Bill, models.CASCADE)
    operat = models.ForeignKey(Operat, models.CASCADE)
    value = models.IntegerField(verbose_name="Поле м-м", blank=True, null=True)

    def __str__(self):
        return "м-м №" + str(self.pk)

    class Meta:
        verbose_name = "м-м"
        db_table = "bill_operat"