from django import forms
from django.core.validators import RegexValidator

class ZipcodeForm(forms.Form):
    zip_code = forms.CharField(validators=[RegexValidator('^[0-9]{5}(?:-[0-9]{4})?$', message='Enter a valid zipcode.')])

class ProductSearchForm(forms.Form):
    name = forms.CharField(max_length=128)

class StoreSearchForm(forms.Form):
    name = forms.CharField(max_length=128)

class ProductAddForm(forms.Form):
    product_name = forms.CharField(max_length=128)
    price = forms.FloatField(min_value=0)
    store_name = forms.CharField(max_length=128)

class StoreAddForm(forms.Form):
    store_name = forms.CharField(max_length=128)
    address = forms.CharField(max_length=256)
    latitude = forms.FloatField()
    longitude = forms.FloatField()
