from django.urls import path
from employee_time_sheet.views import (
    TableDetail,
    IndexListView,
    TablesList,
    TableCreateView,
    TableEditView,
    choose_staff,
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
        TableCreateView.as_view(),
        name="table_create",
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
        TableEditView.as_view(),
        name="detail_formset",
    ),
]
