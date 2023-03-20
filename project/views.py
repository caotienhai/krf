from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DeleteView, DetailView, CreateView, UpdateView
from bootstrap_datepicker_plus.widgets import DatePickerInput
from django.urls import reverse_lazy
from django.db.models import Avg
from .models import Project, Task
from .forms import ProjectRegistrationForm, TaskRegistrationForm

        
class ProjectListView(LoginRequiredMixin, ListView):
    template_name = 'project/projects.html'    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        context['avg_projects'] = Project.objects.all().aggregate(Avg('complete_per'))['complete_per__avg']
        context['tasks'] = Task.objects.all()
        context['overdue_tasks'] = Task.objects.all().filter(due='Overdue')
        return context
     
    def get_queryset(self):
        if self.request.user.is_superuser:
            projects = Project.objects.all().order_by('-dead_line')
        else:            
            projects = Project.objects.all().filter(assign = self.request.user)
        return projects.order_by('-dead_line')    
    
class ProjectDetailView(LoginRequiredMixin,DetailView): 
    model = Project      
    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView,self).get_context_data(**kwargs)
        return context
        
    def get_queryset(self):
        queryset = super(ProjectDetailView,self).get_queryset().filter(pk=self.kwargs.get('pk'))        
        return queryset

class ProjectUpdateView(LoginRequiredMixin,UpdateView):    
    model = Project    
    fields = '__all__'
    success_url = reverse_lazy('projects:list')
    
    def get_form(self):
        form = super().get_form()
        form.fields['dead_line'].widget = DatePickerInput()
        return form
    
    def get_context_data(self, **kwargs):
        context = super(ProjectUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Update Project'

        return context
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(pk=self.kwargs.get('pk'))
    
    def form_valid(self, form):
        project = Project.objects.filter(pk=self.kwargs['pk'])[0]
        self.object = form.save(commit=False)
        self.object.save() 
        return redirect('projects:project_tasks', project.id)
               
@login_required
def my_tasks(request):
    if request.user.is_superuser: 
        tasks = Task.objects.all().order_by('project')
    else:
        tasks = Task.objects.all().filter(assign = request.user).order_by('project')
    avg_tasks = tasks.aggregate(Avg('complete_per'))['complete_per__avg']
    overdue_tasks = tasks.filter(due='Overdue')
    context = {
        'avg_tasks' : avg_tasks,
        'tasks' : tasks,
        'overdue_tasks' : overdue_tasks,
    } 
    return render(request, 'project/task_list.html', context)

class ProjectCreateView(LoginRequiredMixin,CreateView):
    model = Project
    fields = '__all__'    
    success_url = reverse_lazy('projects:list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)       
        context['title'] = 'Add New Project'
        context['form'] = ProjectRegistrationForm()

        #context['named_formsets'] = self.get_named_formsets()

        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save() 
        return redirect(self.get_success_url())

#View detailed task of a projects
@login_required
def project_tasks(request,pk):    
    choosen_project=Project.objects.get(pk=pk)
    project_tasks=Task.objects.filter(project=choosen_project).order_by('dead_line').select_related('project')
    return render(request, 'project/project_tasks.html',{
        'project_tasks':project_tasks, 'choosen_project': choosen_project,
        })
     
class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    success_url = reverse_lazy('projects:list')

    def get_queryset(self):
        queryset = super(ProjectDeleteView, self).get_queryset()
        return queryset.filter(pk=self.kwargs.get('pk'))
    
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class TaskCreateView(LoginRequiredMixin,CreateView):
    model = Task
    fields = ('assign','task_name','task_target','task_update','complete_per','dead_line','status','due') 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)       
        context['title'] = 'Add New Task'
        context['form'] = TaskRegistrationForm()
        context['project'] = get_object_or_404(Project,pk=self.kwargs['pk'])

        return context

    def form_valid(self, form):
        project = Project.objects.filter(pk=self.kwargs['pk'])[0]
        self.object = form.save(commit=False)
        self.object.project = project
        self.object.save() 
        return redirect('projects:project_tasks', project.id)

class TaskUpdateView(LoginRequiredMixin,UpdateView):
    model = Task    
    fields = ('assign','task_name','task_target','task_update','complete_per','dead_line','status','due')    
    
    def get_form(self):
        form = super().get_form()
        form.fields['dead_line'].widget = DatePickerInput()
        return form
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Task'
        context['project'] = get_object_or_404(Project,pk=self.kwargs['project_pk'])
        
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        pk = self.kwargs['pk']
        queryset = queryset.filter(pk=pk)
        return queryset
    
    def form_valid(self, form):
        project = get_object_or_404(Project,pk=self.kwargs['project_pk'])
        self.object = form.save(commit=False)
        self.object.project = project
        self.object.save()
        return redirect('projects:project_tasks', project.pk)


@login_required
def delete_task(request, pk):    
    task = Task.objects.get(id=pk)
    pkk = task.project.id 
    task.delete()
    messages.success(
            request, 'Task have been deleted successfully'
            )
    return redirect('projects:project_tasks', pkk)

@login_required
def done_task(request, pk):    
    task = Task.objects.get(id=pk)
    pkk = task.project.id
    Task.objects.filter(id=pk).update(status='Done')
    messages.success(
            request, 'Task done successfully'
            )
    return redirect('projects:project_tasks', pkk)