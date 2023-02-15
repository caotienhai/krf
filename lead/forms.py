from django import forms
from django_countries.fields import CountryField
from .models import Lead, Comment, LeadFile

INPUT_CLASS = 'w-full my-4 py-4 px-6 rounded-xl bg-gray-100'

class AddLeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ('contact_name','company_name','address','country','phone','email','profile','priority','status')
        """widgets = {
            'contact_name': forms.TextInput(attrs={'class':'form-control'}),
            'company_name': forms.TextInput(attrs={'class':'form-control'}),
            'address': forms.TextInput(attrs={'class':'form-control'}),
            'country': forms.Select(attrs={'class':'form-control'}),
            'phone': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.TextInput(attrs={'class':'form-control'}),
            'profile': forms.Textarea(attrs={'class':'form-control'}),
            'priority': forms.Select(attrs={'class':'form-control'}),
            'status': forms.Select(attrs={'class':'form-control'})
        }"""
        
class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment        
        fields = ('content',)
        
class AddFileForm(forms.ModelForm):
    class Meta:
        model = LeadFile        
        fields = ('file',)
