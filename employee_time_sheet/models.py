from django.contrib.auth import get_user_model
from django.db import models
from logistics.models import UnitOrganization
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Table(models.Model):
    unit_organization = models.ForeignKey(
        UnitOrganization,
        on_delete=models.PROTECT,
        related_name="tabel_ucheta_rabochego_vremeni_t12",
    )

    class Meta:
        verbose_name = "Таблица учёта рабочего времени"
        verbose_name_plural = "Таблицы учёта рабочего времени"


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

    class Meta:
        verbose_name = "Строка таблицы учёта рабочего времени"
        verbose_name_plural = "Строки таблицы учёта рабочего времени"


class status(models.TextChoices):
    CAME_TO_WORK = "came_to_work", _("Came_to_work")
    NO_CAME_TO_WORK = "no_came_to_work", _("no_came_to_work")


class Day(models.Model):
    row = models.ForeignKey(Row, on_delete=models.CASCADE, related_name="days")
    day = models.DateField(blank=True, null=True, verbose_name="День")
    status = models.CharField(
        max_length=20,
        choices=status.choices,
    )
