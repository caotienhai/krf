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
    path('<int:pk>/convert/',views.ConvertView.as_view(), name='convert'),
    path('add-lead/',views.LeadCreateView.as_view(), name='add'),
    path('search-lead',views.SearchLead.as_view(), name='search_lead'),
    path('import-lead/',views.importLead, name='import'),
]
