from django import forms

from pledge.models import Pledge

class PledgeForm(forms.ModelForm):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={"style": "width: 167px"}))
    areacode = forms.CharField(required=True, widget=forms.TextInput(attrs={"style":"width: 35px"}))
    phone_number = forms.CharField(required=True, widget=forms.TextInput(attrs={"style":"width: 89px"}))
    class Meta:
        model = Pledge
        fields = ("name", "areacode", "phone_number")