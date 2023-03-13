from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

status = (
    ('Stuck', 'Stuck'),
    ('Working', 'Working'),
    ('Done', 'Done'),
)

due = (
    ('On Due', 'On Due'),
    ('Overdue', 'Overdue'),
    ('Done', 'Done'),
)

class Project(models.Model):
    name = models.CharField(max_length=80)
    slug = models.SlugField('shortcut', blank=True)
    assign = models.ForeignKey(User,related_name='projects',null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=7, choices=status, default='Working')
    objective = models.TextField(blank=True)
    dead_line = models.DateField(blank=True, null=True)    
    complete_per = models.FloatField(default=0,max_length=2, validators = [MinValueValidator(0), MaxValueValidator(100)])
    description = models.TextField(blank=True)
    project_link = models.URLField(blank=True)
    add_date = models.DateField(auto_now_add=True)
    upd_date = models.DateField(auto_now_add=False, auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return (self.name)


class Task(models.Model):
    project = models.ForeignKey(Project, related_name='tasks', on_delete=models.CASCADE)
    assign = models.ForeignKey(User,related_name='tasks',null=True, on_delete=models.SET_NULL)
    task_name = models.CharField(max_length=80)
    task_target = models.TextField(blank=True)
    dead_line = models.DateField(blank=True, null=True)
    task_update = models.TextField(blank=True)
    complete_per = models.FloatField(default=0,max_length=2, validators = [MinValueValidator(0), MaxValueValidator(100)])
    status = models.CharField(max_length=7, choices=status, default=1)
    due = models.CharField(max_length=7, choices=due, default=1)

    class Meta:
        ordering = ['project', 'task_name']

    def __str__(self):
        return(self.task_name)
    
