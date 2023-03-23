import csv, openpyxl
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django_filters.views import FilterView
from django.views.generic import DetailView, DeleteView, UpdateView, CreateView
from .models import Client, Team, ClientFilter, User
from .forms import AddCommentForm, AddFileForm

@login_required 
def clients_export(request):
    if request.user.username == 'haict':
        clients = Client.objects.all()
    else:
        clients = Client.objects.filter(assign_to = request.user)
    response = HttpResponse(
        content_type = 'text/csv',
        headers = {'Content-Disposition': 'attachment; filename = "clientexpport.csv"'},
    )
    writer = csv.writer(response)
    writer.writerow(['Client','Company','Address','Country','profile','PIC','Team','Created by','Created at'])
    for client in clients:
        writer.writerow([client.contact_name,client.company_name,client.address,client.country,client.profile,client.assign_to,client.team.name,client.created_by,client.created_at])
    
    return response

class AddCommentView(LoginRequiredMixin,View):
    def post(self,request,*args, **kwargs):
        pk= self.kwargs.get('pk')
        form=AddCommentForm(request.POST)
        
        if form.is_valid():
            team=Team.objects.filter(members__id=self.request.user.id)[0]
            comment=form.save(commit=False)
            comment.team = team
            comment.created_by = request.user
            comment.client_id=pk 
            comment.save()
            
        return redirect('clients:detail',pk=pk)
    
class AddFileView(LoginRequiredMixin,View):    
    def post(self,request,*args, **kwargs):
        pk= self.kwargs.get('pk')
        form=AddFileForm(request.POST,request.FILES)
        
        if form.is_valid():
            file=form.save(commit=False)
            file.created_by = request.user
            file.client_id=pk
            file.save()
            
        return redirect('clients:detail',pk=pk)

class ClientListView(LoginRequiredMixin,FilterView):
    paginate_by = 10
    model = Client
    template_name = 'client/client_list.html'
    context_object_name='clients'
    filter_class = ClientFilter
     
    def get_queryset(self):
        team = Team.objects.filter(members__id=self.request.user.id)[0]
        queryset = super(ClientListView, self).get_queryset().order_by('country')
        if team.name == 'Operation' or self.request.user.is_superuser:
            return queryset.all()
        elif self.request.user.groups.all()[0].name == 'teamlead':
            return queryset.filter(team = team)
        else:
            return queryset.filter(assign_to = self.request.user)
        
class ClientDetailView(LoginRequiredMixin,DetailView): 
    model = Client
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['commentform'] = AddCommentForm()
        context['fileform'] = AddFileForm()
        context['title'] = 'View Client Details'
        return context
        
    def get_queryset(self):
        queryset = super(ClientDetailView, self).get_queryset()
        return queryset.filter(pk=self.kwargs.get('pk'))
        
class ClientCreateView(LoginRequiredMixin,CreateView):
    model = Client    
    success_url = reverse_lazy('clients:list')
    fields = ('contact_name','company_name','address','country','region','phone','email','profile','care_update','portfolio','source','team','assign_to','created_by',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Customer'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return redirect(self.get_success_url())
        
class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('clients:list')
    
    def get_queryset(self):
        queryset = super(ClientDeleteView, self).get_queryset()
        if self.request.user.username == 'haict':
            return queryset.filter(pk=self.kwargs.get('pk'))
        else:
            return queryset.filter(assign_to=self.request.user, pk=self.kwargs.get('pk'))
    
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class ClientUpdateView(LoginRequiredMixin,UpdateView):
    model = Client    
    fields = ('contact_name','company_name','address','country','region','phone','email','profile','care_update','portfolio','source','team','assign_to','created_by',)
    success_url = reverse_lazy('clients:list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Client'
        context['commentform'] = AddCommentForm()
        context['fileform'] = AddFileForm()
        return context
    
    def get_queryset(self):
        queryset = super(ClientUpdateView, self).get_queryset()
        return queryset.filter(pk=self.kwargs.get('pk'))
  
@login_required 
def importClient(request):
    if request.method == 'POST':
        if 'myfile' in request.FILES:
            excel_file = request.FILES['myfile']
            wb = openpyxl.load_workbook(excel_file)
            worksheet = wb['Sheet1']
            data = list()
            for row in worksheet.iter_rows(min_row=2, max_row=worksheet.max_row):
                client = Client()
                team=Team.objects.filter(name=row[0].value)[0]
                client.team = team
                client.contact_name = row[1].value
                client.company_name = row[2].value
                client.address = row[3].value
                client.country = row[4].value
                client.region = row[5].value
                client.phone = row[6].value
                client.email = row[7].value
                client.profile = row[8].value
                client.care_update = row[9].value
                client.portfolio = row[10].value
                client.source = row[11].value
                pic=User.objects.filter(username=row[12].value)[0]
                client.assign_to = pic
                client.created_by = request.user
                data.append(client)
                
            Client.objects.bulk_create(data)
            return redirect('clients:list')
        else:
            messages.warning(request, message='Failed to upload data!')
            return render(request, 'client/client_import.html')
    else:
        return render(request, 'client/client_import.html')