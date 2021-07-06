from django.contrib.auth import get_user_model
from django.db import models
from logistics.models import UnitOrganization

User = get_user_model()


class TabelUchetaRabochegoVremeniT12(models.Model):
    unit_organization = models.ForeignKey(
        UnitOrganization,
        on_delete=models.PROTECT,
        related_name="tabel_ucheta_rabochego_vremeni_t12",
    )

    class Meta:
        verbose_name = "Таблица учёта рабочего времени"
        verbose_name_plural = "Таблицы учёта рабочего времени"


class RowOfTabelUchetaRabochegoVremeni(models.Model):
    staff = models.ForeignKey(
        User,
        related_name="row_table_ucheta_rabochego_vremeni",
        on_delete=models.DO_NOTHING,
    )
    table = models.ForeignKey(
        TabelUchetaRabochegoVremeniT12,
        on_delete=models.CASCADE,
        related_name="rows",
    )

    class Meta:
        verbose_name = "Строка таблицы учёта рабочего времени"
        verbose_name_plural = "Строки таблицы учёта рабочего времени"
