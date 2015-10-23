from django import forms

class ZipcodeForm(forms.Form):
    zip_code = forms.IntegerField(label="Zipcode", max_value=100000, min_value=10000)

