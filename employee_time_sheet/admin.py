from django.contrib import admin
from employee_time_sheet.models import (
    RowOfTabelUchetaRabochegoVremeni,
    TabelUchetaRabochegoVremeniT12,
)

admin.site.register(RowOfTabelUchetaRabochegoVremeni)
admin.site.register(TabelUchetaRabochegoVremeniT12)
