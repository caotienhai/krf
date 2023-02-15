from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from .models import Lead, Team
from client.models import Client, Comment as ClientComment, ClientFile
from .forms import AddCommentForm, AddFileForm, AddLeadForm

class LeadListView(LoginRequiredMixin,ListView):
    model = Lead
    
    def get_queryset(self):
        queryset = super(LeadListView, self).get_queryset()
        return queryset.filter(created_by = self.request.user, converted_to_client = False)
    
class LeadDetailView(LoginRequiredMixin,DetailView): 
    model = Lead
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AddCommentForm()
        context['fileform'] = AddFileForm()
        return context
        
    def get_queryset(self):
        queryset = super(LeadDetailView, self).get_queryset()        
        return queryset.filter(created_by=self.request.user,pk=self.kwargs.get('pk'))

class LeadUpdateView(LoginRequiredMixin,UpdateView):
    model = Lead    
    fields = ('contact_name','company_name','address','country','phone','email','profile','priority','status',)
    success_url = reverse_lazy('leads:list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Lead'

        return context
    
    def get_queryset(self):
        queryset = super(LeadUpdateView, self).get_queryset()
        return queryset.filter(created_by=self.request.user, pk=self.kwargs.get('pk'))

class LeadCreateView(LoginRequiredMixin,CreateView):
    model = Lead    
    #fields = ('contact_name','company_name','address','country','phone','email','profile','priority','status',)
    success_url = reverse_lazy('leads:list')
    form_class = AddLeadForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = Team.objects.filter(created_by=self.request.user)[0]
        context['team'] = team
        context['title'] = 'Add lead'

        return context

    def form_valid(self, form):
        team = Team.objects.filter(created_by=self.request.user)[0]

        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.team = team
        self.object.save()
        
        return redirect(self.get_success_url())
    
class LeadDeleteView(LoginRequiredMixin, DeleteView):
    model = Lead
    success_url = reverse_lazy('leads:list')

    def get_queryset(self):
        queryset = super(LeadDeleteView, self).get_queryset()
        return queryset.filter(created_by=self.request.user, pk=self.kwargs.get('pk'))
    
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class AddCommentView(LoginRequiredMixin,View):
    def post(self,request,*args, **kwargs):
        pk= self.kwargs.get('pk')
        form=AddCommentForm(request.POST)
        
        if form.is_valid():
            team=Team.objects.filter(created_by=self.request.user)[0]
            comment=form.save(commit=False)
            comment.team = team
            comment.created_by = request.user
            comment.lead_id=pk
            comment.save()
            
        return redirect('leads:detail',pk=pk)

class AddFileView(LoginRequiredMixin,View):
    
    def post(self,request,*args, **kwargs):
        pk= self.kwargs.get('pk')
        form=AddFileForm(request.POST,request.FILES)
        
        if form.is_valid():
            team=Team.objects.filter(created_by=self.request.user)[0]
            file=form.save(commit=False)
            file.team = team
            file.created_by = request.user
            file.lead_id=pk
            file.save()
            
        return redirect('leads:detail',pk=pk)


class ConvertView(View):
    def get(self, request, *args, **kwargs):
        pk=self.kwargs.get('pk')        
        lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
        team = Team.objects.filter(created_by=request.user)[0]
        
        client = Client.objects.create(
            team = team,
            contact_name = lead.contact_name,
            company_name = lead.company_name,
            address = lead.address,
            country = lead.country,
            phone = lead.phone,
            email = lead.email,
            profile = lead.profile,
            created_by = request.user,
        ) 
        lead.converted_to_client = True
        lead.status = '5.ordered'
        lead.save()
        
        #convert lead cmt to client cmt
        comments = lead.comments.all()
        for comment in comments:
            ClientComment.objects.create(
                client = client,
                content = comment.content,
                created_by = comment.created_by,
                team = team                
            )

        messages.success(request,'The Lead Has Been Converted!')
        return redirect('leads:list')