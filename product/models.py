from django.db import models
import django_filters
from django.contrib.auth.models import User

class ProductGroup(models.Model):
    group = models.CharField(max_length=20)
    class Meta:
        ordering = ('group',)
    
    def __str__(self) -> str:
        return self.group

class ProductModel(models.Model):
    model = models.CharField(max_length=20)
    model_description = models.TextField(blank=True,null=True)
    class Meta:
        ordering = ('model',)
    
    def __str__(self) -> str:
        return self.model
        
class Product(models.Model):    
    CHOICE_CAT = (('RO standard', 'RO standard'),
                  ('RO Cabinet', 'RO Cabinet'),
                  ('Dispenser', 'Dispenser'),
                  ('RO commercial', 'RO commercial'),
                  ('Air industry','Air industry'),
                  ('Accessories','Accessories'),
                  ('Air industry','Air industry'),
                  ('Pet filter','Pet filter'),
                  ('Other','Other'),)    

    CHOICE_STATUS = (('Active', 'Active'),                                          
                     ('Inactive', 'Inactive'),('Canceled', 'Canceled'),)
    product_code = models.CharField(max_length=10,unique=True)
    product_name = models.CharField(max_length=50,unique=True)
    english_name = models.CharField(max_length=50,unique=True)
    description = models.TextField(blank=True,null=True)
    category = models.CharField(max_length=20,choices=CHOICE_CAT)
    group = models.ForeignKey(ProductGroup,related_name='products',blank=True,null=True, on_delete=models.SET_NULL)    
    model = models.ForeignKey(ProductModel,related_name='products',blank=True,null=True, on_delete=models.SET_NULL)
    packing_type = models.CharField(max_length=50,blank=True,null=True)
    brand = models.CharField(max_length=20,blank=True,null=True)
    unit_cost = models.IntegerField(blank=True,null=True, default=0)
    qty_per_ctn = models.IntegerField(blank=True,null=True, default=1)
    ctn_length = models.IntegerField(blank=True,null=True, default=300)
    ctn_width = models.IntegerField(blank=True,null=True, default=300)
    ctn_height = models.IntegerField(blank=True,null=True, default=300)
    status = models.CharField(max_length=24,choices=CHOICE_STATUS,default='Active')
    created_by = models.ForeignKey(User, related_name='products',default='haict',on_delete=models.SET_DEFAULT)
    created_at = models.DateTimeField(auto_now_add=True)
    modify_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('product_code',)
    
    def __str__(self) -> str:
        return self.english_name
    
class ProductFile(models.Model):    
    product = models.ForeignKey(Product, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='productfiles') 
    created_by = models.ForeignKey(User, related_name='product_files', default='haict', on_delete=models.SET_DEFAULT)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.product.english_name
    
class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = ['category']