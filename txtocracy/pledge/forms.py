from django import forms

from pledge.models import Pledge

class PledgeForm(forms.ModelForm):
    areacode = forms.CharField(required=True, widget=forms.TextInput(attrs={"size":3}))
    phone_number = forms.CharField(required=True, widget=forms.TextInput(attrs={"size":7}))
    class Meta:
        model = Pledge
        fields = ("name", "areacode", "phone_number")