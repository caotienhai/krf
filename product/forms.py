from django import forms
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Product, ProductFile

class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = reverse_lazy('index')
        self.helper.form_method = 'GET'
        self.helper.add_input(Submit('submit','Submit'))
    class Meta:
        model = Product
        fields = ('product_code', 'product_name','english_name','category',
              'model','brand','group','unit_cost','status','description',
              'packing_type','qty_per_ctn','ctn_length','ctn_width','ctn_height')

        
        
class AddProductFileForm(forms.ModelForm):
    class Meta:
        model = ProductFile
        fields = ('file',)