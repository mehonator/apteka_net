from django.urls import path
from employee_time_sheet.views import (
    TablesUchetaRabochegoVremeniDetail,
    TablesUchetaRabochegoVremeniList,
    table_ucheta_rabochego_vremeni_create,
)

app_name = "employee_time_sheet"
urlpatterns = [
    path(
        "<slug:unit_organization>/tables_ucheta_rabochego_vremeni_list/",
        TablesUchetaRabochegoVremeniList.as_view(),
        name="tables_ucheta_rabochego_vremeni_list",
    ),
    path(
        "tables_ucheta_rabochego_vremeni_detail/<int:pk>/",
        TablesUchetaRabochegoVremeniDetail.as_view(),
        name="tables_ucheta_rabochego_vremeni_detail",
    ),
    path(
        "<slug:unit_organization>/tables_ucheta_rabochego_vremeni_create/",
        table_ucheta_rabochego_vremeni_create,
        name="table_ucheta_rabochego_vremeni_create",
    ),
]
