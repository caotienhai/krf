from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.ProjectListView.as_view(), name='list'),
    path('create-project/', views.ProjectCreateView.as_view(), name='create_project'),
    path('<int:pk>/', views.project_tasks, name='project_tasks'),
    path('<int:pk>/edit/',views.ProjectUpdateView.as_view(), name='project_update'),
    path('<int:pk>/delete/', views.ProjectDeleteView.as_view(), name='delete'),
    path('<int:pk>/create-task/', views.TaskCreateView.as_view(), name='create_task'),
    path('tasks/', views.my_tasks, name='task'),
    path('<int:project_pk>/tasks/<int:pk>/update/', views.TaskUpdateView.as_view(), name='task_update'),
    path('<int:pk>/delete-task/', views.delete_task, name='delete_task'),
    path('<int:pk>/done-task/', views.done_task, name='done_task'),
] 