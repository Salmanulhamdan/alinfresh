from django import forms
from coreapp.models import Coupons
class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupons
        fields = '__all__'  
        widgets = {
            'valid_from': forms.DateInput(attrs={'type': 'date'}),
            'valid_to': forms.DateInput(attrs={'type': 'date'}),
        }  
from django import forms

class DateFilterForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))