from django.contrib.auth import get_user_model
from django.db import models
from logistics.models import UnitOrganization
from django.utils.translation import gettext_lazy as _
import calendar
from datetime import datetime


User = get_user_model()


def get_first_day_of_month(instance):
    return datetime(instance.year, instance.month, 1)


class Table(models.Model):
    unit_organization = models.ForeignKey(
        UnitOrganization,
        on_delete=models.PROTECT,
        related_name="tabel_ucheta_rabochego_vremeni_t12",
    )

    year = models.IntegerField(default=datetime.now().year)
    month = models.IntegerField(default=datetime.now().month)

    first_day = models.DateField(
        verbose_name="Первый день",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.unit_organization.name} {self.year} {self.month}"

    class Meta:
        unique_together = ["unit_organization", "year", "month"]
        verbose_name = "Таблица учёта рабочего времени"
        verbose_name_plural = "Таблицы учёта рабочего времени"


def fill_first_day(instance, created, raw, **kwargs):
    if not created or raw:
        return

    date = datetime(instance.year, instance.month, 1)
    instance.first_day = date
    instance.save()


models.signals.post_save.connect(
    fill_first_day, sender=Table, dispatch_uid="fill_first_day"
)


class Row(models.Model):
    staff = models.ForeignKey(
        User,
        related_name="row_table_ucheta_rabochego_vremeni",
        on_delete=models.DO_NOTHING,
    )
    table = models.ForeignKey(
        Table,
        on_delete=models.CASCADE,
        related_name="rows",
    )

    def __str__(self):
        return f"{self.table} {self.staff.get_full_name()}"

    class Meta:
        unique_together = ["staff", "table"]
        verbose_name = "Строка таблицы учёта рабочего времени"
        verbose_name_plural = "Строки таблицы учёта рабочего времени"


class Status(models.TextChoices):
    CAME_TO_WORK = "came_to_work", _("Явился")
    NO_CAME_TO_WORK = "no_came_to_work", _("Не явился")
    NOT_INFO = "not_info", _("Нет информации")


class Day(models.Model):
    row = models.ForeignKey(Row, on_delete=models.CASCADE, related_name="days")
    day = models.DateField(blank=True, null=True, verbose_name="День")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        blank=True,
        null=True,
    )

    def get_rus_status(self):
        return self.status[1]

    def __str__(self):
        return f"{self.day} {self.status} {self.row}"


def create_days(instance, created, raw, **kwargs):
    if not created or raw:
        return

    year = instance.table.year
    month = instance.table.month
    _, number_days_in_month = calendar.monthrange(year, month)
    for numer_day in range(1, number_days_in_month + 1):
        day = datetime(year, month, numer_day)
        Day.objects.get_or_create(
            row=instance,
            status=Status.NOT_INFO,
            day=day.date(),
        )


models.signals.post_save.connect(
    create_days, sender=Row, dispatch_uid="create_days"
)
