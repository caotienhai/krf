from django import forms
from .models import Comment, LeadFile
        
class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment        
        fields = ('content',)
        
class AddFileForm(forms.ModelForm):
    class Meta:
        model = LeadFile        
        fields = ('file',)