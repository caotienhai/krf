from django import forms
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Lead, Comment, LeadFile

INPUT_CLASS = 'w-full my-4 py-4 px-6 rounded-xl bg-gray-100'

class AddLeadForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = reverse_lazy('index')
        self.helper.form_method = 'GET'
        self.helper.add_input(Submit('submit','Submit'))
        
    class Meta:
        model = Lead
        fields = '__all__'
        
class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment        
        fields = ('content',)
        
class AddFileForm(forms.ModelForm):
    class Meta:
        model = LeadFile        
        fields = ('file',)