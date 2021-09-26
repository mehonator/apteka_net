from typing import Dict, List

from django.shortcuts import get_list_or_404

from employee_time_sheet.models import Day, Row
from employee_time_sheet.models import Table as TimeTable


def get_data_for_file_time_table(table: TimeTable) -> List[Dict]:
    rows = get_list_or_404(Row, table=table)
    users_days: List[Dict] = []
    for row in rows:
        username = row.staff.get_full_name()
        days = list(get_list_or_404(Day, row=row))
        day_status = [day.get_status_display() for day in days]
        users_days.append(
            {
                "username": username,
                "days_status": day_status,
            }
        )
    return users_days
