from django.db import models
import django_filters
from django_countries.fields import CountryField
from django.contrib.auth.models import User
from team.models import Team

class Lead(models.Model):
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
    CHOICE_PRIORITY = (('low', 'low'),('medium', 'medium'),('high', 'high'),)    
    CHOICE_STATUS = (('1.follow-up', '1.follow-up'),                                          
                     ('2.demanded', '2.demanded'),
                     ('3.offered', '3.offered'),
                     ('4.dealing', '4.dealing'),
                     ('5.ordered', '5.ordered'),
                     ('6.lost', '6.lost'),)
    team = models.ForeignKey(Team, related_name='leads', on_delete=models.DO_NOTHING)
    contact_name = models.CharField(max_length=50, default='unknown')
    company_name = models.CharField(max_length=70, unique=True)
    address = models.CharField(max_length=100,blank=True,null=True)
    country = CountryField(blank=True,null=True)
    region = models.CharField(max_length=10,choices=CHOICE_REG,default='GCC')
    phone = models.CharField(max_length=50,blank=True,null=True)
    email = models.EmailField(blank=True,null=True)
    profile = models.TextField(blank=True,null=True)
    care_update = models.TextField(blank=True,null=True)
    portfolio = models.CharField(max_length=50,blank=True,null=True, choices=CHOICE_PORTFOLIO)
    priority = models.CharField(max_length=10,choices=CHOICE_PRIORITY,default='medium')
    status = models.CharField(max_length=14,choices=CHOICE_STATUS,default='2.demanded')
    source = models.CharField(max_length=50,blank=True,null=True, choices=CHOICE_SOURCE)
    converted_to_client = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='leads',on_delete=models.DO_NOTHING)
    assign_to = models.ForeignKey(User, related_name='lead_pic',on_delete=models.SET_DEFAULT, default=1)
    created_at = models.DateField(auto_now_add=True)
    modify_at = models.DateField(auto_now=True)
     
    class Meta:
        ordering = ('company_name',)
    
    def __str__(self) -> str:
        return self.company_name
    
class Comment(models.Model):
    team = models.ForeignKey(Team, related_name='lead_comments', on_delete=models.CASCADE)
    lead = models.ForeignKey(Lead, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField(blank=True,null=True)
    created_by = models.ForeignKey(User, related_name='lead_comments', on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.lead.company_name
    
class LeadFile(models.Model):
    team = models.ForeignKey(Team, related_name='lead_files',on_delete=models.CASCADE)
    lead = models.ForeignKey(Lead, related_name='lead_files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='leadfiles')
    created_by = models.ForeignKey(User, related_name='lead_files', on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.lead.company_name

class Contact(models.Model):
    CHOICE_REL = (('Muslim','Muslim'),('Hindi','Hindi'),
                  ('Buddhism','Buddhism'),('Christian','Christian'),
                  ('Other','Other'),)
    CHOICE_DISC = (('Dominance','Dominance'),('Influence','Influence'),
                  ('Steadiness','Steadiness'),('Compliance','Compliance'),)
    
    team = models.ForeignKey(Team, related_name='lead_contacts', on_delete=models.SET_DEFAULT, default=1)
    assign_to = models.ForeignKey(User, related_name='lead_pics',on_delete=models.SET_DEFAULT, default=1)
    lead = models.ForeignKey(Lead, related_name='contacts', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50,blank=True,null=True)
    last_name = models.CharField(max_length=50,blank=True,null=True)
    birth_date = models.DateField(blank=True,null=True)
    married = models.BooleanField(default=False)
    family = models.CharField(max_length=100,blank=True,null=True)
    phone_number = models.CharField(max_length=50,blank=True,null=True)
    email = models.EmailField(blank=True,null=True)
    religion = models.CharField(max_length=10,choices=CHOICE_REL,default='Muslim')
    disc = models.CharField(max_length=15,choices=CHOICE_DISC,default='Dominance')
    stakeholders = models.TextField(blank=True,null=True)    
    gains = models.TextField(blank=True,null=True)
    pains = models.TextField(blank=True,null=True)

class LeadFilter(django_filters.FilterSet):
    class Meta:
        model = Lead
        fields = ['country','region','portfolio','source','priority','status']