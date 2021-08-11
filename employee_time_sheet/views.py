from typing import List, Dict
from django.contrib.auth import get_user_model
from django.forms.formsets import BaseFormSet
from django.forms.models import inlineformset_factory, modelformset_factory
from django.forms import formset_factory
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView
from django.urls import reverse
from django.http import HttpResponseBadRequest

from employee_time_sheet.forms import (
    RowForm,
    TabbleForm,
    DayForm,
    ChooseStaffForm,
)
from employee_time_sheet.models import Day, Row, Table
from logistics.models import UnitOrganization


User = get_user_model()


class TablesList(ListView):
    model = Table
    context_object_name = "tables"
    template_name = "employee_time_sheet/tables_list.html"

    def get_queryset(self):
        unit_organization = get_object_or_404(
            UnitOrganization, slug=self.kwargs.get("unit_organization")
        )
        result = unit_organization.tabel_ucheta_rabochego_vremeni_t12.all()

        return result


def tables_list(request, unit_organization):
    if request.method == "GET":
        unit_organization = get_object_or_404(
            UnitOrganization, slug=unit_organization
        )
        tables = unit_organization.tabel_ucheta_rabochego_vremeni_t12.all()
        context = {
            "tables": tables,
            "unit_organization": unit_organization,
        }
        return render(
            request,
            "employee_time_sheet/tables_list.html",
            context,
        )


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


def validate_staff_form(parsed_form):
    for key, value in parsed_form.items():
        if not User.objects.filter(pk=value["pk_staff"]).exists():
            return False
    return True


ChooseStaffFormset = formset_factory(ChooseStaffForm, extra=0)


def tables_add_in_unit(request, unit_organization):
    if request.method == "GET":
        unit_organization = get_object_or_404(
            UnitOrganization, slug=unit_organization
        )
        staff = unit_organization.profiles_staff.all()
        staff_init = []
        for one_of_staff in staff:
            initial_data = {
                "pk_staff": one_of_staff.pk,
                "full_name": one_of_staff.user.get_full_name,
                "choosen": True,
            }

            staff_init.append(initial_data)

        choose_staff_formset = ChooseStaffFormset(initial=staff_init)
        context = {
            "unit_organization": unit_organization,
            "staff": staff,
            "choose_staff_formset": choose_staff_formset,
        }
        return render(
            request,
            "employee_time_sheet/tables_add.html",
            context,
        )

    elif request.method == "POST":
        parsed_staff = parse_choose_staff(request.POST)
        if not validate_staff_form(parsed_staff):
            return HttpResponseBadRequest(
                content="Данные пользователи не прошли валидацию",
                status=400,
            )

        unit_organization = get_object_or_404(
            UnitOrganization, slug=unit_organization
        )
        table = Table.objects.create(unit_organization=unit_organization)
        for one_of_staff in parsed_staff.values():
            staff = get_object_or_404(User, pk=one_of_staff["pk_staff"])
            Row.objects.create(table=table, staff=staff)

        return HttpResponseRedirect(reverse("employee_time_sheet:index"))


class TableDetail(DetailView):
    model = Table
    context_object_name = "table"
    template_name = (
        "employee_time_sheet/table_ucheta_rabochego_vremeni_detail.html"
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["rows"] = self.object.rows.all()
        return context


def index(request):
    if request.method == "GET":
        units_organizations = UnitOrganization.objects.all()
        return render(
            request,
            "employee_time_sheet/index.html",
            context={"units_organizations": units_organizations},
        )


FullTable = inlineformset_factory(
    Table,
    Row,
    fields=("staff",),
)


def table_ucheta_rabochego_vremeni_create(request):
    if request.method == "POST":
        table_form = TabbleForm(request.POST)
        row_form = RowForm(request.POST)
        full_table = FullTable(request.POST)
    else:
        table_form = TabbleForm()
        row_form = RowForm()
        full_table = FullTable()
    context = {
        "table_form": table_form,
        "row_form": row_form,
        "full_table": full_table,
    }

    return render(
        request,
        "employee_time_sheet/tables_ucheta_rabochego_vremeni_create.html",
        context=context,
    )


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


def prepare_update_days_from_parse_form(days_ids_statuses) -> List[Day]:
    days = []
    for day_id_status in days_ids_statuses:
        day = get_object_or_404(Day, pk=day_id_status["id"])
        day.status = day_id_status["status"]
        days.append(day)
    return days


def detail_formset(request, pk: int):
    if request.method == "POST":
        days_ids_statuses = parse_form_time_sheet(request.POST)
        days = prepare_update_days_from_parse_form(days_ids_statuses)
        Day.objects.bulk_update(days, ["status"])
        return HttpResponseRedirect(
            reverse("employee_time_sheet:detail_formset", kwargs={"pk": pk})
        )
    else:
        table = get_object_or_404(Table, pk=pk)
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
            "employee_time_sheet/"
            "table_ucheta_rabochego_vremeni_detail formset.html",
            context=context,
        )
