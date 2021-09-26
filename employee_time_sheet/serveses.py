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


def parse_form_time_sheet(post_days) -> list:
    nums_statuses = {}
    nums_ids = {}
    for form in post_days:
        if "form" in form:
            _, num, attribute = form.split("-")
            if attribute == "id":
                nums_ids[num] = post_days[form]
            elif attribute == "status":
                nums_statuses[num] = post_days[form]

    ids_statuses = []
    for num, id in nums_ids.items():
        ids_statuses.append(
            {"id": int(id), "status": nums_statuses[num]},
        )

    return ids_statuses


def parse_choose_staff(post_data) -> Dict[str, Dict[str, str]]:
    parsed_data: Dict[str, Dict[str, str]] = {}
    for key, value in post_data.items():
        splited_key = key.split("-")
        if splited_key[0] == "form":
            id_form = splited_key[1]
            attr = splited_key[2]

            if parsed_data.get(id_form) is None:
                parsed_data[id_form] = {attr: value}
            else:
                parsed_data[id_form].update({attr: value})
    return parsed_data


def get_init_data_choose_staf(staff, is_choosen: bool) -> List[Dict]:
    staff_init = []
    for one_of_staff in staff:
        initial_data = {
            "pk_staff": one_of_staff.pk,
            "full_name": one_of_staff.get_full_name,
            "is_choosen": is_choosen,
        }

        staff_init.append(initial_data)
    return staff_init
