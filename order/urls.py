from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('',views.OrderListView.as_view(), name='list'),
    path('<int:id>/',views.order_items, name='items'),
    path('<int:pk>/delete/',views.OrderDeleteView.as_view(), name='delete'),
    path('<int:pk>/delete-detail/', views.delete_detail, name='delete_detail'),
    path('<int:pk>/edit/',views.OrderUpdateView.as_view(), name='edit'),
    path('add-order/',views.OrderCreateView.as_view(), name='add'),
    
]
