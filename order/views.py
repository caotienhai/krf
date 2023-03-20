from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from decimal import *
from django.contrib import messages
from django.urls import reverse_lazy
from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from django_filters.views import FilterView
from django.views.generic import DetailView, DeleteView, UpdateView, CreateView
from .models import Order, OrderDetail, Team, OrderFilter
from .forms import OrderForm, DetailFormSet

class OrderInline():
    form_class = OrderForm
    model = Order
    template_name = 'order/order_inline.html'
    
    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        self.object = form.save()
        
        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        return redirect('orders:edit',self.object.id)
    
    def formset_details_valid(self, formset):
        details = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        ordersum = 0
        ordercbm = 0
        ordercost = 0
        pkk=0 
        for detail in details:
            detail.order = self.object
            detail.save()
                   
            if not detail.FOC:
                ordersum+=detail.quantity*detail.unit_price
            ordercbm+=detail.quantity/detail.product_code.qty_per_ctn*detail.product_code.ctn_length*detail.product_code.ctn_width*detail.product_code.ctn_height/1000000000
            ordercost+=detail.quantity*detail.product_code.unit_cost
            pkk=detail.order_number.id
        Order.objects.filter(id = pkk).update(order_total = ordersum, order_cbm = ordercbm, order_cost = ordercost)
        
    
class OrderListView(LoginRequiredMixin,FilterView):
    paginate_by = 10
    model = Order
    template_name = 'order/order_list.html'
    context_object_name='orders'
    filter_class = OrderFilter
    def get_queryset(self):
        team = Team.objects.filter(members__id=self.request.user.id)[0]
        queryset = Order.objects.all()
        if self.request.user.is_superuser or team.name == 'Operation':
            return queryset.order_by('-load_date') 
        elif self.request.user.groups.all()[0].name=='teamlead':
            return queryset.filter(team = team).order_by('-load_date') 
        else:
            return queryset.filter(pic = self.request.user).order_by('-load_date') 
        
class OrderDetailView(LoginRequiredMixin,DetailView): 
    model = Order      
    def get_context_data(self, **kwargs):
        context = super(OrderDetailView,self).get_context_data(**kwargs)
        return context
        
    def get_queryset(self):
        queryset = super(OrderDetailView,self).get_queryset().select_related(
            'client', 'pic', 'team', 'ship_line').filter(pk=self.kwargs.get('pk'))        
        return queryset

#View detailed order items
def order_items(request,id):    
    order=Order.objects.select_related('pic','client','team','ship_line').get(pk=id)
    orderitems=OrderDetail.objects.filter(order_number=order).order_by('id').select_related('order_number','product_code')
    payment = order.payment1+order.payment2
    
    return render(request, 'order/order_items.html',{
        'orderitems':orderitems, 'order': order, 'payment':payment
        })
    
class OrderUpdateView(OrderInline,LoginRequiredMixin,UpdateView):    
 
    def get_context_data(self, **kwargs):
        context = super(OrderInline, self).get_context_data(**kwargs)
        context['title'] = 'Update order'
        context['named_formsets'] = self.get_named_formsets()

        return context

    def get_named_formsets(self):
        return {
            'details': DetailFormSet(self.request.POST or None, 
                                     self.request.FILES or None, 
                                     instance=self.object, 
                                     prefix='details'),
        }

class OrderCreateView(LoginRequiredMixin,CreateView):
    model = Order
    fields = '__all__'    
    success_url = reverse_lazy('orders:list')
    def get_form(self):
        form = super().get_form()
        form.fields['deposit_date'].widget = DateTimePickerInput()
        form.fields['payment1_date'].widget = DateTimePickerInput()
        form.fields['payment2_date'].widget = DateTimePickerInput()
        form.fields['load_date'].widget = DateTimePickerInput()
        form.fields['etd_date'].widget = DateTimePickerInput()
        form.fields['invoice_date'].widget = DateTimePickerInput()
        form.fields['declare_date'].widget = DateTimePickerInput()
        return form    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)       
        context['title'] = 'Add order'
        #context['named_formsets'] = self.get_named_formsets()

        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user        
        self.object.save()
        
        return redirect(self.get_success_url())
    
    #def get_named_formsets(self):
    #    if self.request.method == "GET":
    #        return {
    #            'details': DetailFormSet(prefix='details'),
    #        }
    #    else:
    #        return {
    #            'details': DetailFormSet(self.request.POST or None, self.request.FILES or None, prefix='details'),
    #        }
            
class OrderDeleteView(LoginRequiredMixin, DeleteView):
    model = Order
    success_url = reverse_lazy('orders:list')

    def get_queryset(self):
        queryset = super(OrderDeleteView, self).get_queryset()
        return queryset.filter(pk=self.kwargs.get('pk'))
    
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

def delete_detail(request, pk):
    
    detail = OrderDetail.objects.get(id=pk)
    pkk = detail.order_number.id
    od=Order.objects.get(id = pkk)
    if not detail.FOC: 
        od.order_total = Decimal(od.order_total) - Decimal(detail.get_total_price)
    od.order_cbm -= Decimal(detail.get_item_cbm)
    od.order_cost -= Decimal(detail.get_item_cost)
    od.save()
    detail.delete()
    messages.success(
            request, 'Order item have been deleted successfully'
            )
    return redirect('orders:edit', pkk)