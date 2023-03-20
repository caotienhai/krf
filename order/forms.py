from django import forms
from bootstrap_datepicker_plus.widgets import DatePickerInput
from django.forms import inlineformset_factory
from .models import Order, OrderDetail

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('order_number','client','pic','team','ship_country','status',
                  'deposit','deposit_date','payment1','payment1_date','payment2','payment2_date',
                  'load_date','etd_date','eta_date','booking','discount','freight','ship_line',
                  'trucking_fee','local_charge','invoice_number','invoice_date','declaration','declare_date')
        widgets = {
            'deposit_date':DatePickerInput(),
            'payment1_date':DatePickerInput(),
            'payment2_date':DatePickerInput(),
            'load_date':DatePickerInput(),
            'etd_date':DatePickerInput(),
            'invoice_date':DatePickerInput(),
            'declare_date':DatePickerInput(),
        }
class OrderItemForm(forms.ModelForm):
      class Meta:
        model = OrderDetail
        fields = ('product_code','quantity','unit_price','FOC','item_status','created_by')
                        
DetailFormSet = inlineformset_factory(
    Order, OrderDetail, form=OrderItemForm, extra=0, can_delete=True, can_delete_extra=True
)
