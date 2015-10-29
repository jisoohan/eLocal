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
    price = forms.FloatField(min_value=0)
    def __init__(self, *args, **kwargs):
        super(ProductAddForm, self).__init__(*args, **kwargs)
        self.fields['store_name'] = forms.ChoiceField(choices=ElocalUtils.getStoreChoices())

class StoreAddForm(forms.Form):
    store_name = forms.CharField(max_length=128)
    street_number = forms.CharField(max_length=10, required=False)
    street_address = forms.CharField(max_length=256)
    city = forms.CharField(max_length=128)
    state = forms.CharField(max_length=2)
    zip_code = forms.CharField(max_length=10)
    country = forms.CharField(max_length=128)
    has_card = forms.BooleanField()
    sun_open_time = forms.TimeField(widget=SelectTimeWidget(twelve_hr=True, use_seconds=False))
    sun_close_time = forms.TimeField(widget=SelectTimeWidget(twelve_hr=True, use_seconds=False))
    sun_closed = forms.BooleanField()
    mon_open_time = forms.TimeField(widget=SelectTimeWidget(twelve_hr=True, use_seconds=False))
    mon_close_time = forms.TimeField(widget=SelectTimeWidget(twelve_hr=True, use_seconds=False))
    mon_closed = forms.BooleanField()
    tues_open_time = forms.TimeField(widget=SelectTimeWidget(twelve_hr=True, use_seconds=False))
    tues_close_time = forms.TimeField(widget=SelectTimeWidget(twelve_hr=True, use_seconds=False))
    tues_closed = forms.BooleanField()
    wed_open_time = forms.TimeField(widget=SelectTimeWidget(twelve_hr=True, use_seconds=False))
    wed_close_time = forms.TimeField(widget=SelectTimeWidget(twelve_hr=True, use_seconds=False))
    wed_closed = forms.BooleanField()
    thur_open_time = forms.TimeField(widget=SelectTimeWidget(twelve_hr=True, use_seconds=False))
    thur_close_time = forms.TimeField(widget=SelectTimeWidget(twelve_hr=True, use_seconds=False))
    thur_closed = forms.BooleanField()
    fri_open_time = forms.TimeField(widget=SelectTimeWidget(twelve_hr=True, use_seconds=False))
    fri_close_time = forms.TimeField(widget=SelectTimeWidget(twelve_hr=True, use_seconds=False))
    fri_closed = forms.BooleanField()
    sat_open_time = forms.TimeField(widget=SelectTimeWidget(twelve_hr=True, use_seconds=False))
    sat_close_time = forms.TimeField(widget=SelectTimeWidget(twelve_hr=True, use_seconds=False))
    sat_closed = forms.BooleanField()
