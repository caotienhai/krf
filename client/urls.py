from django.urls import path
from . import views

app_name = 'clients'

urlpatterns = [
    path('',views.ClientListView.as_view(), name='list'), 
    path('<int:pk>/',views.ClientDetailView.as_view(), name='detail'),
    path('add-client/',views.ClientCreateView.as_view(), name='add'),
    path('<int:pk>/add-contact/',views.AddContactView.as_view(), name='add_contact'),
    path('contact/',views.ContactList.as_view(), name='contact'),
    path('contact/<int:pk>/detail',views.ContactDetailView.as_view(), name='contact_detail'),
    path('contact/<int:pk>/update',views.ContactUpdateView.as_view(), name='contact_update'),
    path('contact/<int:pk>/delete',views.delete_contact, name='delete_contact'),
    path('<int:pk>/add-comment/',views.AddCommentView.as_view(), name='add_comment'),
    path('<int:pk>/add-file/',views.AddFileView.as_view(), name='add_file'),
    path('<int:pk>/delete/',views.ClientDeleteView.as_view(), name='delete'),
    path('<int:pk>/edit/',views.ClientUpdateView.as_view(), name='edit'),
    path('import-client/',views.importClient, name='import'),
    path('export/',views.clients_export, name='export'),
]
