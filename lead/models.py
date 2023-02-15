from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth.models import User
from team.models import Team

class Lead(models.Model):    
    CHOICE_PRIORITY = (('','Choose Priority'),('low', 'low'),('medium', 'medium'),('high', 'high'),)    
    CHOICE_STATUS = (('', 'Choose lead status'),
                     ('1.follow-up', '1.follow-up'),                                          
                     ('2.demanded', '2.demanded'),
                     ('3.offered', '3.offered'),
                     ('4.dealing', '4.dealing'),
                     ('5.ordered', '5.ordered'),
                     ('6.lost', '6.lost'),)
    team = models.ForeignKey(Team, related_name='leads', on_delete=models.CASCADE)
    contact_name = models.CharField(max_length=50)
    company_name = models.CharField(max_length=70)
    address = models.CharField(max_length=100,blank=True,null=True)
    country = CountryField(blank=True,null=True)
    phone = models.CharField(max_length=50,blank=True,null=True)
    email = models.EmailField(blank=True,null=True)
    profile = models.TextField(blank=True,null=True)
    priority = models.CharField(max_length=10,choices=CHOICE_PRIORITY,default='medium')
    status = models.CharField(max_length=14,choices=CHOICE_STATUS,default='2.demanded')
    converted_to_client = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='leads',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modify_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('contact_name',)
    
    def __str__(self) -> str:
        return self.contact_name
    
class Comment(models.Model):
    team = models.ForeignKey(Team, related_name='lead_comments', on_delete=models.CASCADE)
    lead = models.ForeignKey(Lead, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField(blank=True,null=True)
    created_by = models.ForeignKey(User, related_name='lead_comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.created_by.username
    
class LeadFile(models.Model):
    team = models.ForeignKey(Team, related_name='lead_files', on_delete=models.CASCADE)
    lead = models.ForeignKey(Lead, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='leadfiles')
    created_by = models.ForeignKey(User, related_name='lead_files', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.created_by.username