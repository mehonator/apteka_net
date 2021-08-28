from django import forms
import datetime

from employee_time_sheet.models import Day, Row, Table


class TabbleForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ("unit_organization",)


class RowForm(forms.ModelForm):
    class Meta:
        model = Row
        fields = ("staff",)


class DayForm(forms.ModelForm):
    class Meta:
        model = Day
        fields = ("status",)


class ChooseStaffForm(forms.Form):
    full_name = forms.CharField(
        label="ФИО",
        max_length=512,
        widget=forms.TextInput(attrs={"readonly": "readonly", "size": "50"}),
    )
    is_choosen = forms.BooleanField(
        initial=True, label="Выбран", required=False
    )
    pk_staff = forms.IntegerField(widget=forms.HiddenInput(), required=True)


def get_current_year():
    return datetime.date.today().year


def get_current_month():
    return datetime.date.today().month


class MonthYearForm(forms.Form):
    num_month = forms.IntegerField(
        min_value=1,
        max_value=12,
        initial=get_current_month,
        label="Месяц",
    )
    num_year = forms.IntegerField(
        min_value=2021,
        max_value=2100,
        initial=get_current_year,
        label="Год",
    )
