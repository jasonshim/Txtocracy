from django import forms
from django.core.validators import RegexValidator

from pledge.models import Pledge

IntValidator = RegexValidator(regex=r"^\d*$")

class PhoneInput(forms.TextInput):
    input_type = 'tel'

class PledgeForm(forms.ModelForm):
    name = forms.CharField(required=True,
                           widget=forms.TextInput(attrs={"style": "width: 167px"}))
    areacode = forms.CharField(required=True,
                               max_length=3,
                               min_length=3,
                               widget=PhoneInput(attrs={"style":"width: 35px"}),
                               validators=[IntValidator])
    phone_number = forms.CharField(required=True,
                                        max_length=7,
                                        min_length=7,
                                        widget=PhoneInput(attrs={"style":"width: 89px"}),
                                        validators=[IntValidator])
    class Meta:
        model = Pledge
        fields = ("name", "areacode", "phone_number")