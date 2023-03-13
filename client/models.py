from django.db import models
import django_filters
from django_countries.fields import CountryField
from django.contrib.auth.models import User
from team.models import Team
 

class Client(models.Model):
    CHOICE_REG = (('GCC','GCC'),('MEA','MEA'),
                  ('SA','SA'),('SEA','SEA'),('America','America'),
                  ('Africa','Africa'),('Europe','Europe'),
                  ('East Asia','East Asia'),('Australia','Australia'),)
    CHOICE_PORTFOLIO = (('Household RO','Household RO'),
                        ('Electric Appliances','Electric Appliances'),
                        ('Commercial RO','Commercial RO'),('Construction/Sanitary','Construction/Sanitary'),
                        ('Others','Others'))
    CHOICE_SOURCE = (('Alibaba','Alibaba'),('WATI','WATI'),
                     ('Google','Google'),('Trade Fairs','Trade Fairs'),
                     ('Custom Data','Custom Data'),('Others','Others'),)
    team = models.ForeignKey(Team, related_name='clients', on_delete=models.CASCADE)
    contact_name = models.CharField(max_length=50)
    company_name = models.CharField(max_length=70, unique=True)
    address = models.CharField(max_length=100,blank=True,null=True)
    country = CountryField(blank=True,null=True)
    region = models.CharField(max_length=10,choices=CHOICE_REG,default='GCC')
    phone = models.CharField(max_length=50,blank=True,null=True)
    email = models.EmailField(blank=True,null=True)
    profile = models.TextField(blank=True,null=True)
    care_update = models.TextField(blank=True,null=True)
    portfolio = models.CharField(max_length=50,blank=True,null=True, choices=CHOICE_PORTFOLIO)
    source = models.CharField(max_length=50,blank=True,null=True, choices=CHOICE_SOURCE)
    created_by = models.ForeignKey(User, related_name='clients',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modify_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('contact_name',)
    
    def __str__(self) -> str:
        return self.contact_name
    
class Comment(models.Model):
    team = models.ForeignKey(Team, related_name='client_comments', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField(blank=True,null=True)
    created_by = models.ForeignKey(User, related_name='client_comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.client.company_name
    
class ClientFile(models.Model):
    team = models.ForeignKey(Team, related_name='client_files', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='clientfiles')
    created_by = models.ForeignKey(User, related_name='client_files', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.client.company_name
    
class ClientFilter(django_filters.FilterSet):
    class Meta:
        model = Client
        fields = ['country','region','portfolio','source']