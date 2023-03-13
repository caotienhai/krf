from django.db import models
import django_filters
from django_countries.fields import CountryField
from decimal import *
from django.contrib.auth.models import User
from product.models import Product
from client.models import Client
from team.models import Team

class ShipLines(models.Model):
    line_name = models.CharField(max_length=20, unique=True)
    tracking_link = models.URLField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    class Meta:
        ordering = ('line_name',)
    
    def __str__(self) -> str:
        return self.line_name

class Order(models.Model):
    
    CHOICE_STATUS = (('','Choose Status'),('drafted','drafted'),('opened','opened'),
                     ('shipped','shipped'),('closed','closed'),('on hold','on hold'),)
    
    order_number = models.CharField(max_length=20, unique=True)
    client = models.ForeignKey(Client,related_name='orders',default='Example Company',on_delete=models.SET_DEFAULT)
    pic = models.ForeignKey(User,related_name='orders',default='haict',on_delete=models.SET_DEFAULT)
    team = models.ForeignKey(Team,related_name='orders',null=True,on_delete=models.SET_NULL)
    order_date = models.DateField(auto_now_add=True)
    load_date = models.DateField(null=True,blank=True)
    etd_date = models.DateField(null=True,blank=True)
    eta_date = models.DateField(null=True,blank=True)
    deposit = models.DecimalField(default=0, decimal_places=2, max_digits=9)
    deposit_date = models.DateField(null=True,blank=True)
    payment1 = models.DecimalField(default=0, decimal_places=2, max_digits=9)
    payment1_date = models.DateField(null=True,blank=True)
    payment2 = models.DecimalField(default=0, decimal_places=2, max_digits=9)
    payment2_date = models.DateField(null=True,blank=True)
    discount = models.DecimalField(default=0, decimal_places=2, max_digits=9)
    order_total = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    freight = models.DecimalField(default=0, decimal_places=2, max_digits=9)
    order_cbm = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    order_cost = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    booking = models.CharField(max_length=30,null=True,blank=True)
    ship_line = models.ForeignKey(ShipLines,related_name='orders',null=True,blank=True,on_delete=models.SET_NULL)
    ship_country = CountryField(null=True,blank=True)
    trucking_fee = models.IntegerField(default=0)
    local_charge = models.IntegerField(default=0)
    invoice_number = models.CharField(max_length=20,null=True,blank=True)
    invoice_date = models.DateField(null=True,blank=True)
    declaration = models.CharField(max_length=30,null=True,blank=True)
    declare_date = models.DateField(null=True,blank=True)
    status = models.CharField(max_length=14,choices=CHOICE_STATUS,default='drafted')
    
    class Meta:
        ordering = ('order_number',)
    
    def __str__(self) -> str:
        return self.order_number
        
class OrderDetail(models.Model): 
 
    CHOICE_STATUS = (('', 'Choose item status'),('Confirmed', 'Confirmed'),                                          
                     ('Temporary', 'Temporary'),('SXXK', 'SXXK'),)
    order_number = models.ForeignKey(Order,related_name='orderdetails', on_delete=models.CASCADE)
    product_code = models.ForeignKey(Product, related_name='orderdetails',null=True,on_delete=models.SET_NULL)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=6,decimal_places=2,null=True)
    FOC = models.BooleanField(default=False)

    @property
    def get_total_price(self):
        if self.FOC:
            total_price = 0
            return total_price
        else:
            total_price = self.quantity*self.unit_price
            return round(total_price,2)

    @property
    def get_item_cbm(self):
        item_cbm = self.quantity/self.product_code.qty_per_ctn*self.product_code.ctn_length*self.product_code.ctn_width*self.product_code.ctn_height/1000000000
        return round(item_cbm,2)

    @property
    def get_item_cost(self):
        item_cost = self.quantity*self.product_code.unit_cost/23500
        return round(item_cost,2)

    item_status = models.CharField(max_length=24,choices=CHOICE_STATUS,default='Temporary')    
    created_by = models.ForeignKey(User, related_name='orderdetails',default='haict',on_delete=models.SET_DEFAULT)
    created_at = models.DateTimeField(auto_now_add=True)
    modify_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('product_code',)
    
    def __str__(self) -> str:
        return  "Order: "+self.order_number.order_number +"  " + self.product_code.product_name +"  - Qty: " + str(self.quantity)

class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = ['ship_country'] 