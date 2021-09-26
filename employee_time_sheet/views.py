import csv
import datetime
from io import BytesIO
from typing import Dict, List, Tuple

import pyexcel as pe
from django.contrib.auth import get_user_model
from django.forms import formset_factory
from django.forms.formsets import BaseFormSet
from django.forms.models import modelformset_factory
from django.http import FileResponse, HttpResponseBadRequest
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.base import View
from logistics.models import Profile, UnitOrganization

from employee_time_sheet.forms import ChooseStaffForm, DayForm, MonthYearForm
from employee_time_sheet.models import Day, Row
from employee_time_sheet.models import Table as TimeTable
from employee_time_sheet.serveses import (get_data_for_file_time_table,
                                          get_init_data_choose_staf,
                                          parse_form_time_sheet)

User = get_user_model()


class TablesList(ListView):
    model = TimeTable
    context_object_name = "tables"
    template_name = "employee_time_sheet/tables_list.html"

    def get_queryset(self):
        unit_organization = get_object_or_404(
            UnitOrganization, slug=self.kwargs.get("unit_organization")
        )
        return unit_organization.tabel_ucheta_rabochego_vremeni_t12.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        unit_organization = get_object_or_404(
            UnitOrganization, slug=self.kwargs["unit_organization"]
        )
        context["unit_organization"] = unit_organization
        return context


def validate_staff_form(parsed_form):
    for key, value in parsed_form.items():
        if not User.objects.filter(pk=value["pk_staff"]).exists():
            return False
    return True


class TableCreateView(View):
    ChooseStaffFormset = formset_factory(ChooseStaffForm, extra=0)

    def get(self, request, *args, **kwargs):
        unit_organization = get_object_or_404(
            UnitOrganization, slug=self.kwargs["unit_organization"]
        )
        staff_profile = unit_organization.profiles_staff.all()
        staff = User.objects.filter(profile__in=staff_profile)
        staff_init = get_init_data_choose_staf(staff, is_choosen=True)
        choose_staff_formset = self.ChooseStaffFormset(initial=staff_init)
        month_year_form = MonthYearForm()
        context = {
            "unit_organization": unit_organization,
            "staff": staff,
            "choose_staff_formset": choose_staff_formset,
            "month_year_form": month_year_form,
        }
        return render(
            request,
            "employee_time_sheet/tables_add.html",
            context,
        )

    def post(self, request, *args, **kwargs):
        parsed_staff = parse_choose_staff(request.POST)
        if not validate_staff_form(parsed_staff):
            return HttpResponseBadRequest(
                content="Данные пользователи не прошли валидацию",
                status=400,
            )

        month_year_form = MonthYearForm(request.POST)
        if not month_year_form.is_valid():
            return HttpResponseBadRequest(
                content="Данные месяца и года не прошли валидацию",
                status=400,
            )

        first_day_month = datetime.date(
            year=month_year_form.cleaned_data["num_year"],
            month=month_year_form.cleaned_data["num_month"],
            day=1,
        )
        if TimeTable.objects.filter(first_day=first_day_month).exists():
            return HttpResponseBadRequest(
                content="Уже существует таблица для этого месяца",
                status=400,
            )

        unit_organization = get_object_or_404(
            UnitOrganization, slug=self.kwargs["unit_organization"]
        )
        table = TimeTable.objects.create(
            unit_organization=unit_organization,
            year=month_year_form.cleaned_data["num_year"],
            month=month_year_form.cleaned_data["num_month"],
        )
        for one_of_staff in parsed_staff.values():
            staff = get_object_or_404(User, pk=one_of_staff["pk_staff"])
            Row.objects.create(table=table, staff=staff)

        return HttpResponseRedirect(reverse("employee_time_sheet:index"))


class TableDetailView(DetailView):
    model = TimeTable
    context_object_name = "table"
    template_name = (
        "employee_time_sheet/table_ucheta_rabochego_vremeni_detail.html"
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["rows"] = self.object.rows.all()
        return context


def generate_csv_time_sheet(table: TimeTable):
    name_unit = table.unit_organization.name
    year = table.year
    month = table.month

    name_table_file = f"{name_unit}{year}{month}.csv"
    rows = get_list_or_404(Row, table=table)
    users_days: List[Dict] = []
    for row in rows:
        username = row.staff.get_full_name()
        days = list(get_list_or_404(Day, row=row))
        days_status = [day.get_status_display() for day in days]
        users_days.append(
            {
                "username": username,
                "days_status": days_status,
            }
        )

    with open(name_table_file, "w", newline="") as csvfile:
        temp_csv_writer = csv.writer(
            csvfile, delimiter=" ", quotechar="|", quoting=csv.QUOTE_MINIMAL
        )
        for user_day in users_days:
            temp_csv_writer.writerow(
                [user_day["username"]] + [user_day["days_status"]]
            )

    return name_table_file


class GetODFTable(View):
    def get(self, request, *args, **kwargs):
        table = get_object_or_404(TimeTable, pk=kwargs["pk"])
        name_unit = table.unit_organization.name
        year = table.year
        month = table.month
        users_days_status = get_data_for_file_time_table(table)
        prepared_data = []
        for user_day in users_days_status:
            prepared_data.append(
                [user_day["username"], *user_day["days_status"]]
            )
        io = BytesIO()
        sheet = pe.Sheet(prepared_data)
        io = sheet.save_to_memory("ods", io)
        response = FileResponse(
            io,
            content_type="text/ods",
            filename=f"{name_unit} {year} {month}.ods",
        )

        return response


class IndexListView(ListView):
    model = UnitOrganization
    template_name = "employee_time_sheet/index.html"

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return []
        profile = self.request.user.profile
        return profile.units_organizations.all()


def prepare_update_days_from_parse_form(days_ids_statuses) -> List[Day]:
    days = []
    for day_id_status in days_ids_statuses:
        day = get_object_or_404(Day, pk=day_id_status["id"])
        day.status = day_id_status["status"]
        days.append(day)
    return days


class TableEditView(View):
    def get(self, request, *args, **kwargs):
        table = get_object_or_404(TimeTable, pk=self.kwargs["pk"])
        rows = table.rows.all()
        rows_names_and_days_formsets: List[Dict[str, BaseFormSet]] = []
        DayFormset = modelformset_factory(model=Day, form=DayForm, extra=0)
        for row in rows:
            days = Day.objects.filter(row=row)
            days_formset = DayFormset(queryset=days)
            names_days_formset = {
                "name": row.staff.get_full_name(),
                "days_formset": days_formset,
            }
            rows_names_and_days_formsets.append(names_days_formset)

        context = {
            "table": table,
            "rows": rows,
            "rows_names_and_days_formsets": rows_names_and_days_formsets,
        }

        return render(
            request,
            "employee_time_sheet/table_edit.html",
            context=context,
        )

    def post(self, request, *args, **kwargs):
        days_ids_statuses = parse_form_time_sheet(request.POST)
        days = prepare_update_days_from_parse_form(days_ids_statuses)
        Day.objects.bulk_update(days, ["status"])
        return HttpResponseRedirect(
            reverse(
                "employee_time_sheet:detail", kwargs={"pk": self.kwargs["pk"]}
            )
        )


def get_chosen_and_unchosen(staff_data: List[Dict]) -> Tuple:
    pks_chosen = []
    pks_unchosen = []
    for one_of_staff in staff_data:
        if one_of_staff["is_choosen"]:
            pks_chosen.append(one_of_staff["pk_staff"])
        else:
            pks_unchosen.append(one_of_staff["pk_staff"])
    chosens = User.objects.filter(pk__in=pks_chosen)
    unchosens = User.objects.filter(pk__in=pks_unchosen)
    return chosens, unchosens


def add_rows(users, table):
    for user in users:
        Row.objects.update_or_create(staff=user, table=table)


def del_rows(users, table):
    Row.objects.filter(staff__in=users, table=table).delete()


def choose_staff(request, pk: int):
    ChooseStaffFormset = formset_factory(ChooseStaffForm, extra=0)
    if request.method == "GET":
        table = get_object_or_404(TimeTable, pk=pk)

        selected_staff = User.objects.filter(
            row_table_ucheta_rabochego_vremeni__in=table.rows.all()
        )
        selected_profile = Profile.objects.filter(user__in=selected_staff)
        unselected_staff = User.objects.filter(
            profile__units_organizations=table.unit_organization
        ).exclude(profile__in=selected_profile)

        init_data_staff = get_init_data_choose_staf(
            selected_staff, is_choosen=True
        )
        init_data_staff += get_init_data_choose_staf(
            unselected_staff, is_choosen=False
        )

        choose_staff_formset = ChooseStaffFormset(initial=init_data_staff)
        context = {"choose_staff_formset": choose_staff_formset}
        return render(
            request, "employee_time_sheet/tables_choose_staff.html", context
        )

    elif request.method == "POST":
        input_choose_staff_formset = ChooseStaffFormset(request.POST)
        if input_choose_staff_formset.is_valid():
            table = get_object_or_404(TimeTable, pk=pk)
            chosens, unchosens = get_chosen_and_unchosen(
                input_choose_staff_formset.cleaned_data
            )
            add_rows(chosens, table)
            del_rows(unchosens, table)

            return HttpResponseRedirect(
                reverse("employee_time_sheet:detail", kwargs={"pk": pk})
            )
