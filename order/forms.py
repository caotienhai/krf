from django import forms
from django.forms import inlineformset_factory
from .models import Order, OrderDetail

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('order_number','client','pic','team','ship_country','status',
                  'deposit','deposit_date','payment1','payment1_date','payment2','payment2_date',
                  'load_date','etd_date','eta_date','booking','discount','freight',
                  'trucking_fee','local_charge','invoice_number','invoice_date','declaration','declare_date')

class OrderItemForm(forms.ModelForm):
      class Meta:
        model = OrderDetail
        fields = ('product_code','quantity','unit_price','FOC','item_status','created_by')
                        
DetailFormSet = inlineformset_factory(
    Order, OrderDetail, form=OrderItemForm, extra=0, can_delete=True, can_delete_extra=True
)
