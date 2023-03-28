from django import forms
from bootstrap_datepicker_plus.widgets import DatePickerInput
from .models import Comment, LeadFile, Contact
        
class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment        
        fields = ('content',)
        
class AddFileForm(forms.ModelForm):
    class Meta:
        model = LeadFile        
        fields = ('file',)
        
class AddContactForm(forms.ModelForm):
    class Meta:
        model = Contact        
        fields = ['first_name','last_name','lead',
                  'birth_date','married','family','phone_number','email','religion',
                  'disc','gains','pains','stakeholders',
                  'assign_to','team']
        widgets = {
            'birth_date':DatePickerInput(),
        }