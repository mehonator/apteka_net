from employee_time_sheet.models import Table
from django.views.generic import DetailView, ListView


class TablesUchetaRabochegoVremeniList(ListView):
    model = Table
    context_object_name = "tables"
    template_name = (
        "employee_time_sheet/tables_ucheta_rabochego_vremeni_list.html"
    )


class TablesUchetaRabochegoVremeniDetail(DetailView):
    model = Table
    context_object_name = "table"
    template_name = (
        "employee_time_sheet/table_ucheta_rabochego_vremeni_detail.html"
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["rows"] = self.object.rows.all()
        return context
