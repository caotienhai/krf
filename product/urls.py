from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('',views.ProductListView.as_view(), name='list'),
    path('<int:pk>/',views.ProductDetailView.as_view(), name='detail'),
    path('<int:pk>/delete/',views.ProductDeleteView.as_view(), name='delete'),
    path('<int:pk>/edit/',views.ProductUpdateView.as_view(), name='edit'),
    path('<int:pk>/add-file/',views.AddProductFileView.as_view(), name='add_file'),
    path('add-product/',views.ProductCreateView.as_view(), name='add'),
    
]
