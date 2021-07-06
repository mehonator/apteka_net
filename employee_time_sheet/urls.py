from django.urls import path
from employee_time_sheet.views import (
    TablesUchetaRabochegoVremeniDetail,
    TablesUchetaRabochegoVremeniList,
)

app_name = "employee_time_sheet"
urlpatterns = [
    path(
        "tables_ucheta_rabochego_vremeni_list/",
        TablesUchetaRabochegoVremeniList.as_view(),
        name="tables_ucheta_rabochego_vremeni_list",
    ),
    path(
        "tables_ucheta_rabochego_vremeni_detail/<int:pk>/",
        TablesUchetaRabochegoVremeniDetail.as_view(),
        name="tables_ucheta_rabochego_vremeni_detail",
    ),
]
