from django.contrib.auth.models import User
from django.db import models



class Team(models.Model):    
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User,related_name='teams', null=True, blank=True)
    created_by = models.ForeignKey(User,related_name='created_teams',on_delete=models.CASCADE,null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.name

