from django.urls import path
from employee_time_sheet.views import (
    TableDetail,
    table_ucheta_rabochego_vremeni_create,
    detail_formset,
    index,
    tables_add_in_unit,
    tables_list,
)

app_name = "employee_time_sheet"
urlpatterns = [
    path(
        "",
        index,
        name="index",
    ),
    path(
        "<slug:unit_organization>/",
        tables_list,
        name="tables_list",
    ),
    path(
        "<slug:unit_organization>/add/",
        tables_add_in_unit,
        name="table_add_in_unit",
    ),
    path(
        "detail/<int:pk>/",
        TableDetail.as_view(),
        name="detail",
    ),
    path(
        "detail_formset/<int:pk>/",
        detail_formset,
        name="detail_formset",
    ),

    path(
        "<slug:unit_organization>/tables_ucheta_rabochego_vremeni_create/",
        table_ucheta_rabochego_vremeni_create,
        name="table_ucheta_rabochego_vremeni_create",
    ),
]
