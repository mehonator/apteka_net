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
        fields = ("status",)


class ChooseStaffForm(forms.Form):
    full_name = forms.CharField(
        label="ФИО",
        max_length=512,
        widget=forms.TextInput(attrs={"readonly": "readonly", "size": "50"}),
    )
    choosen = forms.BooleanField(initial=True, label="Выбран")
    pk_staff = forms.IntegerField(widget=forms.HiddenInput(), required=True)
