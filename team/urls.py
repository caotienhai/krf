from django.urls import path
from . import views

app_name = 'teams'

urlpatterns = [
    path('<int:pk>/detail/', views.detail, name='detail'),
    path('<int:pk>/edit/', views.edit_team, name='edit'),
]