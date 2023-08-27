from django import forms
from .models import *

class DataItemForm(forms.ModelForm):
    statistic = forms.ModelChoiceField(queryset=Statistic.object.all())
    value = forms.DecimalField()

    class Meta:
        model = DataItem
        fields = ['Statistic', 'value']