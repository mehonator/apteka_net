from django.contrib import admin
from employee_time_sheet.models import (
    Row,
    Table,
    Day,
)


admin.site.register(Table)
admin.site.register(Row)
admin.site.register(Day)
