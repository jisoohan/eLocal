from django import forms
from .utils import ElocalUtils
from eLocal_app.widgets.selecttimewidget import *
from decimal import Decimal

class ZipcodeForm(forms.Form):
    zip_code = forms.CharField(max_length=5)
    radius = forms.ChoiceField(choices=[(x, str(x) + ' miles') for x in range(5, 51, 5)])

class ProductSearchForm(forms.Form):
    name = forms.CharField(max_length=128)

class StoreSearchForm(forms.Form):
    name = forms.CharField(max_length=128)

class ProductAddForm(forms.Form):
    product_name = forms.CharField(max_length=128)
    description = forms.CharField(max_length=1024, widget=forms.Textarea)
    price = forms.DecimalField(decimal_places=2, max_digits=8, min_value=Decimal('0.01'))
    def __init__(self, origin, radius, *args, **kwargs):
        super(ProductAddForm, self).__init__(*args, **kwargs)
        self.fields['store_name'] = forms.ChoiceField(choices=ElocalUtils.getStoreChoices(origin, radius))

class ProductUpdateForm(forms.Form):
    product_name = forms.CharField(max_length=128)
    description = forms.CharField(max_length=1024, widget=forms.Textarea)

class StoreAddForm(forms.Form):
    store_name = forms.CharField(max_length=128)
    street_number = forms.CharField(max_length=10)
    street_address = forms.CharField(max_length=256)
    city = forms.CharField(max_length=60)
    state = forms.CharField(max_length=2)
    zip_code = forms.CharField(max_length=5)
    country = forms.CharField(max_length=2)
    has_card = forms.BooleanField(required=False, initial=False)

class PriceUpdateForm(forms.Form):
    price = forms.FloatField(min_value=0)
