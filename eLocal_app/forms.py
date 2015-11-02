from django import forms
from django.core.validators import RegexValidator
from .utils import ElocalUtils
from eLocal_app.widgets.selecttimewidget import *

class ZipcodeForm(forms.Form):
    zip_code = forms.CharField(validators=[RegexValidator('^[0-9]{5}(?:-[0-9]{4})?$', message='Enter a valid zipcode.')])

class ProductSearchForm(forms.Form):
    name = forms.CharField(max_length=128)

class StoreSearchForm(forms.Form):
    name = forms.CharField(max_length=128)

class ProductAddForm(forms.Form):
    product_name = forms.CharField(max_length=128)
    description = forms.CharField(max_length=1024, widget=forms.Textarea)
    price = forms.FloatField(min_value=0)
    def __init__(self, zip_code, *args, **kwargs):
        super(ProductAddForm, self).__init__(*args, **kwargs)
        self.fields['store_name'] = forms.ChoiceField(choices=ElocalUtils.getStoreChoices(zip_code))

class StoreAddForm(forms.Form):
    store_name = forms.CharField(max_length=128)
    street_number = forms.CharField(max_length=10)
    street_address = forms.CharField(max_length=256)
    city = forms.CharField(max_length=128)
    state = forms.CharField(max_length=2)
    zip_code = forms.CharField(max_length=10)
    country = forms.CharField(max_length=128)
    has_card = forms.BooleanField(required=False, initial=False)
