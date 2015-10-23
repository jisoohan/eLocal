from django import forms
from django.core.validators import RegexValidator

class ZipcodeForm(forms.Form):
    zip_code = forms.CharField(validators=[RegexValidator('^[0-9]{5}(?:-[0-9]{4})?$', message='Enter a valid zipcode.')])

class ProductSearchForm(forms.Form):
    name = forms.CharField()

class StoreSearchForm(forms.Form):
    name = forms.CharField()
