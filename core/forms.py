from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

PAYMENT_CHOICES = (
    ('S','Stripe'),
    ('P','Paypal')
)
class CheckOutForm(forms.Form):
    street_address = forms.CharField(required=False)
    house_address = forms.CharField(required=False)
    city = forms.CharField(required=False)
    country = CountryField(blank_label = '(select country)').formfield(
        required = False,
        widget=CountrySelectWidget(
        attrs = {
            'class':"custom-select d-block w-100"
        }
    ))
    zipcode = forms.CharField(required=False)
    #for billing
