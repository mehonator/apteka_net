from django.urls import path
from .views import (
    index,
    DeleveryList,
    DeleveryDetail,
)

app_name = "logistics"
urlpatterns = [
    path("deleveries/", DeleveryList.as_view(), name="deleveries"),
    path(
        "deleveries/<int:pk>/",
        DeleveryDetail.as_view(),
        name="delevery_detail",
    ),
    path("", index, name="index"),
]
