from django import forms
from crispy_forms.helper import FormHelper
from bootstrap_datepicker_plus.widgets import DatePickerInput
from django.forms import inlineformset_factory
from .models import Project, Task

class TaskRegistrationForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('assign','task_name','task_target','dead_line','task_update','complete_per','status','due')
        widgets = {
            "dead_line": DatePickerInput(),}
        
class ProjectRegistrationForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        widgets = {
            "dead_line": DatePickerInput(),}

TaskFormSet = inlineformset_factory(
    Project, Task, form=TaskRegistrationForm, extra=1, can_delete=True, can_delete_extra=True
)