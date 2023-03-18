from django import forms
from .models import Comment, ClientFile
     
class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        
class AddFileForm(forms.ModelForm):
    class Meta:
        model = ClientFile        
        fields = ('file',)