from django.db.models import query
from django.forms.models import inlineformset_factory, modelformset_factory
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView

from employee_time_sheet.forms import RowForm, TabbleForm, DayForm
from employee_time_sheet.models import Day, Row, Table
from logistics.models import UnitOrganization


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


FullTable = inlineformset_factory(
    Table,
    Row,
    fields=("staff",),
)


def index(request):
    if request.method == "GET":
        units_organizations = UnitOrganization.objects.all()
        return render(
            request,
            "employee_time_sheet/index.html",
            context={"units_organizations": units_organizations},
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


DayFormset = modelformset_factory(
    Day,
    fields=(
        "day",
        "status",
    ),
)


def table_ucheta_rabochego_vremeni_detail_formset(request, pk: int):
    if request.method == "POST":
        pass

    else:
        table = Table.objects.get(pk=pk)
        rows = table.rows.all()
        rows_days_formset = []
        for row in rows:
            row: Day
            days = row.days.all()
            formset = DayFormset(queryset=days)
            for form in formset:
                print(form.as_table())
            rows_days_formset.append(formset)
    formset2 = DayFormset()

    context = {
        "table": table,
        "rows": rows,
        "rows_days_formset": rows_days_formset,
        "formset2": formset2,
    }

    return render(
        request,
        "employee_time_sheet/table_ucheta_rabochego_vremeni_detail formset.html",
        context=context,
    )
