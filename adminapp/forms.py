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
