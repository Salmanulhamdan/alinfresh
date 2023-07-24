from django import forms



from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'payment', 'address', 'order_number', 'order_note', 'order_total', 'tax', 'status', 'ip', 'is_ordered']
