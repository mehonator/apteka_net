from django.urls import path
from employee_time_sheet.views import (
    TableDetail,
    TablesList,
    table_ucheta_rabochego_vremeni_create,
    detail_formset,
    index,
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
        TablesList.as_view(),
        name="tables_list",
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
