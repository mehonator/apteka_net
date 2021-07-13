from django import forms

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
        fields = ("day", "status")
