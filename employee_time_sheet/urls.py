from django.urls import path
from employee_time_sheet.views import (
    TableDetail,
    IndexListView,
    TablesList,
    choose_staff,
    table_ucheta_rabochego_vremeni_create,
    detail_formset,
    tables_add_in_unit,
)

app_name = "employee_time_sheet"
urlpatterns = [
    path(
        "",
        IndexListView.as_view(),
        name="index",
    ),
    path(
        "<slug:unit_organization>/",
        TablesList.as_view(),
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
        "detail/<int:pk>/choose_staff",
        choose_staff,
        name="choose_staff",
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
