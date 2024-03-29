from django.urls import path
from . import views

app_name = 'leads'

urlpatterns = [
    path('',views.LeadListView.as_view(), name='list'),
    path('<int:pk>/',views.LeadDetailView.as_view(), name='detail'),
    path('<int:pk>/delete/',views.LeadDeleteView.as_view(), name='delete'),
    path('<int:pk>/edit/',views.LeadUpdateView.as_view(), name='edit'),
    path('<int:pk>/add-comment/',views.AddCommentView.as_view(), name='add_comment'),
    path('<int:pk>/add-file/',views.AddFileView.as_view(), name='add_file'),
    path('comment/',views.CommentList.as_view(), name='comment'),
    path('<int:pk>/add-contact/',views.AddContactView.as_view(), name='add_contact'),
    path('contact/',views.ContactList.as_view(), name='contact'),
    path('contact/<int:pk>/detail',views.ContactDetailView.as_view(), name='contact_detail'),
    path('contact/<int:pk>/update',views.ContactUpdateView.as_view(), name='contact_update'),
    path('contact/<int:pk>/delete',views.delete_contact, name='delete_contact'),
    path('<int:pk>/convert/',views.ConvertView.as_view(), name='convert'),
    path('add-lead/',views.LeadCreateView.as_view(), name='add'),
    path('search-lead',views.SearchLead.as_view(), name='search_lead'),
    path('import-lead/',views.importLead, name='import'),
]
