from django import forms
from myapp.models import OrderItem

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['item', 'client', 'items_ordered']
        widgets = {
            'client': forms.RadioSelect,
        }
        labels = {
            'items_ordered': 'Quantity',
            'client': 'Client Name',
        }

class InterestForm(forms.Form):
    INTEREST_CHOICES = [
        (1, 'Yes'),
        (0, 'No')
    ]
    interested = forms.TypedChoiceField(
        choices=INTEREST_CHOICES, 
        widget=forms.RadioSelect
    )
    quantity = forms.IntegerField(
        min_value=1, 
        initial=1
    )
    comments = forms.CharField(
        required=False, 
        widget=forms.Textarea, 
        label='Additional Comments'
    )
