from django import forms
from crispy_forms.helper import FormHelper
from django.forms import inlineformset_factory
from .models import Project, Task

class TaskRegistrationForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('assign','task_name','task_target','dead_line','task_update','complete_per','status','due')
 
class ProjectRegistrationForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
    def __init__(self, *args, **kwargs):
            # Add a FormHelper
        self.helper = FormHelper()

        super(ProjectRegistrationForm, self).__init__(*args, **kwargs)

TaskFormSet = inlineformset_factory(
    Project, Task, form=TaskRegistrationForm, extra=1, can_delete=True, can_delete_extra=True
)