from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from django_filters.views import FilterView
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from .models import Product, ProductFilter
from .forms import AddProductFileForm, ProductForm

class ProductListView(LoginRequiredMixin,FilterView):
    paginate_by = 10
    model = Product
    template_name = 'product/product_list.html'
    context_object_name='products'
    filter_class = ProductFilter
    
    def get_queryset(self):
        queryset = super(ProductListView, self).get_queryset()
        return queryset.filter(status = 'Active')
    
class ProductDetailView(LoginRequiredMixin,DetailView): 
    model = Product
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fileform'] = AddProductFileForm()
        return context
        
    def get_queryset(self):
        queryset = super(ProductDetailView, self).get_queryset()        
        return queryset.filter(status = 'Active',pk=self.kwargs.get('pk'))

class ProductUpdateView(LoginRequiredMixin,UpdateView):    
    model = Product    
    fields = ('product_code', 'product_name','english_name','category',
              'model','brand','group','unit_cost','status','description',
              'packing_type','qty_per_ctn','ctn_length','ctn_width','ctn_height')    
    success_url = reverse_lazy('products:list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update product'
        context['fileform'] = AddProductFileForm()

        return context 
    
    def get_queryset(self):
        queryset = super(ProductUpdateView, self).get_queryset()
        return queryset.filter(pk=self.kwargs.get('pk'))
    
    
class ProductCreateView(LoginRequiredMixin,CreateView):
    model = Product    
    fields = ('product_code', 'product_name','english_name','category',
              'model','brand','group','unit_cost','status','description',
              'packing_type','qty_per_ctn','ctn_length','ctn_width','ctn_height')
    success_url = reverse_lazy('products:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)       
        context['title'] = 'Add product'
        return context

    def form_invalid(self, form):
        messages.error(self.request, 'form not valid', 'warning')
        return super().form_invalid(form)
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user        
        self.object.save()             
        return super().form_valid(form)
    
class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('products:list')

    def get_queryset(self):
        queryset = super(ProductDeleteView, self).get_queryset()
        return queryset.filter(pk=self.kwargs.get('pk'))
    
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
    
class AddProductFileView(LoginRequiredMixin,View):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add File'
        
    def post(self,request,*args, **kwargs):
        pk= self.kwargs.get('pk')
        form=AddProductFileForm(request.POST,request.FILES)
        
        if form.is_valid(): 
            file=form.save(commit=False)
            file.created_by = request.user
            file.product_id=pk 
            file.save()
            
        return redirect('products:detail',pk=pk)
