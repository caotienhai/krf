from django import forms
from .models import Comment, ClientFile, Contact
from bootstrap_datepicker_plus.widgets import DatePickerInput
     
class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        
class AddFileForm(forms.ModelForm):
    class Meta:
        model = ClientFile        
        fields = ('file',)
        
class AddContactForm(forms.ModelForm):
    class Meta:
        model = Contact        
        fields = ['first_name','last_name','client',
                  'birth_date','married','family','phone_number','email','religion',
                  'disc','gains','pains','stakeholders',
                  'assign_to','team']
        widgets = {
            'birth_date':DatePickerInput(),
        }