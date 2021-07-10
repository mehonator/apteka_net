from django import forms

from employee_time_sheet.models import Day, Row, Table


class TabbleForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ("unit_organization",)


class RowFoms(forms.ModelForm):
    class Meta:
        model = Row
        fields = ("staff",)
