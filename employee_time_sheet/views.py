from typing import List, Dict, Tuple
from django.contrib.auth import get_user_model
from django.forms.formsets import BaseFormSet
from django.forms.models import modelformset_factory
from django.forms import formset_factory
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView
from django.urls import reverse
from django.http import HttpResponseBadRequest
from django.views.generic.base import View

from employee_time_sheet.forms import (
    DayForm,
    ChooseStaffForm,
)
from employee_time_sheet.models import Day, Row, Table
from logistics.models import Profile, UnitOrganization


User = get_user_model()


class TablesList(ListView):
    model = Table
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

    def post(self, request, *args, **kwargs):
        parsed_staff = parse_choose_staff(request.POST)
        if not validate_staff_form(parsed_staff):
            return HttpResponseBadRequest(
                content="Данные пользователи не прошли валидацию",
                status=400,
            )

        unit_organization = get_object_or_404(
            UnitOrganization, slug=self.kwargs["unit_organization"]
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


class IndexListView(ListView):
    model = UnitOrganization
    template_name = "employee_time_sheet/index.html"

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return []
        profile = self.request.user.profile
        return profile.units_organizations.all()


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


class TableEditView(View):
    def get(self, request, *args, **kwargs):
        table = get_object_or_404(Table, pk=self.kwargs["pk"])
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
        table = get_object_or_404(Table, pk=pk)

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
            table = get_object_or_404(Table, pk=pk)
            chosens, unchosens = get_chosen_and_unchosen(
                input_choose_staff_formset.cleaned_data
            )
            add_rows(chosens, table)
            del_rows(unchosens, table)

            return HttpResponseRedirect(
                reverse("employee_time_sheet:detail", kwargs={"pk": pk})
            )
